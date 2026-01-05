from django.conf import settings
from django.shortcuts import render

# Create your views here.
# topics assessment view 
from users.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef
from quiz.models import TopicsAssessment, QuestionAssessment, ResultAssessment, Course
from django.http import HttpResponseRedirect
import openai

from .models import Question, Topics, TopicsAssessment, QuestionAssessment
from django.contrib import messages


 

#         prompt = f"""
# You are a JSON-only generator.

# Generate exactly {num_topics} course topics for a {course_title} course.

# RULES:
# 1. Always start with the following topics in this exact order:
# 1. "Introduction to {course_title}"
# 2. "Overview – {course_title}" – This should be a short, clear summary without examples or code.
# 3. "Learning Objectives – {course_title}" – This should be a numbered list of at least 12 objectives or more depending on the {category_obj} level, based strictly on the {category_obj} and {difficulty} difficulty. Objective 5 must be a combined title containing the exact titles of Objectives 1, 2, 3, and 4 in order. After listing all objectives, include a concise conclusion paragraph summarizing the overall purpose and importance of mastering these objectives.

# 2. Determine the course type by inspecting the {course_title} (case-insensitive):
# - If {course_title} contains any programming-related keywords (python, javascript, java, c++, c#, php, ruby, html, css, sql, programming, coding, development, data science, machine learning, artificial intelligence, ai, devops, blockchain, software engineering):
#     Use suitable programming learning objectives for {course_title} based on {category_obj} and {difficulty}.
# - If {course_title} contains any non-programming tech-related keywords (tech, technology, digital, IT, cybersecurity, networking, cloud computing, hardware, electronics, gadgets):
#     Use suitable tech learning objectives for {course_title} based on {category_obj} and {difficulty}.
# - Else:
#     Use suitable general learning objectives for {course_title} based on {category_obj} and {difficulty}.

# 3. After the "Learning Objectives – {course_title}" topic:
# - If programming-related:
#     Generate the remaining topics strictly in the order of the learning objectives listed above.
#     For each topic:
#         - Title: Must match the learning objective wording exactly.
#         - Description: Provide a detailed explanation in complete.
#         - Break content down step-by-step.
#         - Include at least 5 fully written, relevant code examples per step with inline comments.
# - If non-programming:
#     Generate the remaining topics strictly in the order of the learning objectives listed above.
#     For each topic:
#         - Title: Must match the learning objective wording exactly.
#         - Description (Rich, instructor-ready): **Write exactly 5 detailed paragraphs** of plain text, totaling between 2000–4000 words. **Do not write more or fewer than 5 paragraphs.** Each paragraph must be substantial, coherent, and directly useful for instruction. Include relevant and related examples in every paragraph to illustrate concepts, ensuring they are practical and applicable to real-world teaching. Use "\\n" for line breaks between paragraphs. Do not use markdown formatting, lists, arrays, or JSON. Ensure the content flows naturally, covers the topic comprehensively, and is instructor-ready, providing explanations, context, and guidance that can be directly incorporated into lessons. Each paragraph should build upon the previous one, creating a coherent and engaging narrative that enhances understanding and demonstrates how the topic can be effectively taught. The AI must strictly adhere to producing exactly 5 paragraphs—no more, no less.
#         - Break content down step-by-step.
#         - Include relevant examples.

# 4. Output must be a single valid JSON array with exactly {num_topics} objects, with only "title" and "description" keys. No explanations, no markdown, no text outside JSON.
# 5. The "description" field must be plain text only, using "\\n" for line breaks. No arrays, no objects, no nested JSON.
# 6. No trailing commas anywhere in the JSON output.
# """

#         prompt = f"""
# You are a JSON-only generator.

# Generate exactly {num_topics} course topics for a {course_title} course.

# RULES:
# 1. Always start with these topics in order:
#    1. "Introduction to {course_title}"
#    2. "Overview – {course_title}" – short, clear summary without examples or code.
#    3. "Learning Objectives – {course_title}" – numbered list of at least 12 objectives. Objective 5 must combine Objectives 1–4. Conclude with a summary paragraph.
#    4. Immediately after "Learning Objectives – {course_title}", the first generated topic must have its title exactly match Learning Objective #1, and its description must directly expand on that objective for learners. Continue in order with each subsequent learning objective becoming the exact title of the next topic.

# 2. Determine course type from {course_title} (case-insensitive):
#    - Programming keywords: python, javascript, java, c++, c#, php, ruby, html, css, sql, programming, coding, development, data science, machine learning, artificial intelligence, ai, devops, blockchain, software engineering.
#    - Non-programming tech keywords: tech, technology, digital, IT, cybersecurity, networking, cloud computing, hardware, electronics, gadgets.
#    - Else: general course.

# 3. After "Learning Objectives – {course_title}":
#    - Programming: generate topics with detailed explanation and at least 5 code examples each.
#    - Non-programming or general: generate topics with **exactly 5 paragraphs per description**, no more, no less. Paragraphs must be:
#        1. Substantial, coherent, and instructor-ready for learners to consume directly.
#        2. Use "\\n" for line breaks between paragraphs.
#        3. Exactly one paragraph among the five MUST contain a numbered bullet-point list.
#         A bullet-point list should have:
#         A short, contextual title line that clearly frames the list in relation to the topic — for example: "Key ethical issues in technology include:" or "Core components of a successful marketing strategy are:"
#         A numbered list in this exact format, with each item starting on its own line:

#         First item
#         Second item
#         Third item
#         Fourth item
#         (and so on, with at least 4 items)
#         No embedding of numbers inside a sentence — the list must be clean and standalone.
#         The contextual title line should immediately precede the list in the same paragraph.

#        4. All other paragraphs must be plain text without bullet points.
#        5. Each paragraph builds on the previous one for a coherent narrative.
#        6. Include relevant, real-world examples in each paragraph.

# 4. At least one paragraph in each topic’s description (preferably the third) must include a real-life teaching story using this structure. introduce the list before listing eg. include:, for example: 
#       - Setup – Introduce the person, company, or setting quickly.
#       - Challenge – The problem they faced (related to the course topic).
#       - Action – What they did.
#       - Outcome – What happened (positive or negative).
#       - Lesson learned – Tie directly back to the teaching point.
#    The story should be engaging but primarily instructional.

# 5. Output: single valid JSON array of {num_topics} objects with keys "title" and "description" only. 
#    - The "title" must exactly match the corresponding Learning Objective text (except for the first three topics).
#    - The "description" should contain the 5 learner-ready paragraphs separated by "\\n".
#    - No markdown, no extra arrays, no nested JSON, no trailing commas.
# """
        
# views.py
from openai import OpenAI
import re
import time
from django.contrib.auth.decorators import user_passes_test
import json
import logging
from django.utils.text import slugify

logger = logging.getLogger(__name__)
from django.http import JsonResponse

from openai import OpenAI
import os

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@login_required
def ai_topics_generator(request):
    if not request.user.is_superuser:
        messages.error(request, "Only superadmins can add topics.")
        return redirect('dashboard')

    categories = Categories.objects.all()
    courses = Courses.objects.all()

    # Save confirmed topics
    if request.method == 'POST' and request.POST.get("confirm_save") == "1":
        total_topics = int(request.POST.get("total_topics", 0))
        category_id = request.POST.get("category_id")
        course_id = request.POST.get("course_id")

        try:
            category_obj = Categories.objects.get(id=category_id)
            course_obj = Courses.objects.get(id=course_id)
        except (Categories.DoesNotExist, Courses.DoesNotExist):
            messages.error(request, "Invalid category or course selected.")
            return redirect('quiz:ai_topics_generator')

        saved = 0
        for i in range(1, total_topics + 1):
            title = request.POST.get(f"title_{i}", "").strip()
            desc = request.POST.get(f"desc_{i}", "").strip()
            transcript = request.POST.get(f"transcript_{i}", "").strip()

            if title and (desc or transcript):
                # Generate slug (same logic your model uses)
                slug = slugify(title)

                topic_obj, created = Topics.objects.update_or_create(
                    slug=slug,
                    courses=course_obj,  # ensures uniqueness per course
                    defaults={
                        'categories': category_obj,
                        'title': title,
                        'desc': desc,
                        'transcript': transcript
                    }
                )
                saved += 1

        messages.success(request, f"{saved} topics saved successfully.")
        return redirect('quiz:ai_topics_generator')

    # Generate topics
    elif request.method == 'POST':
        category_id = request.POST.get('category')
        course_id = request.POST.get('course')
        num_topics = int(request.POST.get('num_topics', 5))
        custom_objectives = request.POST.get('num_objectives', '').strip()  # textarea content
        difficulty = request.POST.get('difficulty', 'medium').lower()
        real_learning_obj = int(request.POST.get('real_learning_obj', 10))

        try:
            category_obj = Categories.objects.get(id=category_id)
            course_obj = Courses.objects.get(id=course_id)
        except (Categories.DoesNotExist, Courses.DoesNotExist):
            messages.error(request, "Invalid category or course selected.")
            return redirect('quiz:ai_topics_generator')

        course_title = course_obj.title or ""
        category_title = (category_obj.name or "").lower().strip()

        # Category-level learning objectives (beginner, intermediate, advanced)
    
        category_rules = {
            "beginner": """
            Focus on foundational knowledge and understanding.
            Use Bloom’s verbs like: define, describe, identify, recognize, explain, understand, list, recall.
            Objectives should be simple, clear, and practical.
            """,
            "intermediate": """
            Focus on applying, analyzing, and comparing.
            Use Bloom’s verbs like: apply, demonstrate, analyze, differentiate, evaluate, design, implement.
            Objectives should link concepts to real-world applications.
            """,
            "advanced": """
            Focus on creating, evaluating, innovating, and leading.
            Use Bloom’s verbs like: evaluate, formulate, create, develop, propose, integrate, critique, synthesize.
            Objectives should include advanced problem-solving, case studies, and professional practice.
            """
        }


        category_instruction = category_rules.get(category_title, category_rules["intermediate"])

        # --- Determine if programming ---
        programming_keywords = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "html", "css", "sql",
            "programming", "coding", "development", "data science", "machine learning",
            "artificial intelligence", "ai", "devops", "blockchain", "software engineering"
        ]
        is_programming = any(kw in course_title.lower() for kw in programming_keywords)

        # Base prompt
        prompt = f"""
        You are a JSON-only generator.
        Generate exactly {num_topics} course topics for a "{course_title}" course under the "{category_title}" category.
        Apply this difficulty setting: {difficulty}.
        {category_instruction}
        """

        # If user provided custom objectives
        if custom_objectives:
            objectives_list = [obj.strip() for obj in custom_objectives.split("\n") if obj.strip()]
            prompt += "\nUse the following learning objectives exactly in this order:\n"
            for i, obj in enumerate(objectives_list, start=1):
                prompt += f"{i}. {obj}\n"

        # Add rules based on course type
    
        # if is_programming:
        #     prompt += f"""
        #     RULES:
        #     1. Always start with these topics in order:
        #     1. "Introduction to {course_title}"
        #     2. "Overview – {course_title}" – short, clear summary without examples or code.
        #     3. "Learning Objectives – {course_title}" – numbered list of at least {real_learning_obj} objectives. Objective 5 must combine Objectives 1-4 into one integrative objective. Conclude with a summary paragraph.
        #     4. Immediately after "Learning Objectives – {course_title}", the first topic title must match Learning Objective #1, with description expanding on it. Continue sequentially for all objectives.

        #     2. For each topic (lesson):
        #     - Provide a **detailed explanation** of the concept.
        #     - Include **at least 5 complete runnable code examples**, each inside triple backticks:

        #         ```python
        #         def explain_python():
        #             return 'Python is widely used in AI due to its simplicity.'
        #         print(explain_python())
        #         ```

        #     - ⚡ If the course is HTML or web-related:
        #         * The "description" field must **never contain raw HTML tags**. 
        #         * Detect **any HTML tag** (headings, links, lists, divs, spans, images, etc.) and always escape them as `&lt;` and `&gt;`.
        #         * This applies everywhere: in normal text, explanations, examples, inline mentions, and pitfalls.

        #         * Only include the **full HTML structure** (`&lt;!DOCTYPE html&gt; ... &lt;/html&gt;`) if the lesson specifically requires a complete page.
        #         * Otherwise, show just the snippet in `<pre><code class="language-html">...</code></pre>`.

        #     - Provide **solutions** for any exercises or challenges mentioned, also wrapped in triple backticks.
        #     - Give **real-world examples** showing where this concept is applied.
        #     - Explain common mistakes or pitfalls learners should avoid.
           

        #     3. Output must be a **single valid JSON array** of {num_topics} objects with keys `"title"` and `"description"` only.
        #     - The `"description"` must:
        #         * Escape all double quotes `"` as `\\"`
        #         * Escape backslashes `\` as `\\\\`
        #         * Escape newlines as `\\n`
        #         * Escape all HTML tags as `&lt;` and `&gt;`
        #     - No trailing commas.
        #     - No commentary or explanation outside the JSON.
        #     - No raw `<h1>`, `<p>`, `<div>`, `<a>`, `<img>`, `<h3>`, etc.
        #     - Use **triple backticks for programming code** and `<pre><code class="language-html"> ... </code></pre>` for HTML examples.

        #     4 At the **end of every lesson**, include a **Mini Project** section:
        #     * Clearly describe the project goal.
        #     * Break it into simple steps for the learner.
        #     * Provide starter/scaffolding code in a code block (if helpful).
        #     * Show the **final full solution** in a code block.
        #     """


        if is_programming:
            prompt += f"""
          RULES (STRICT JSON-SAFE):

            1. Always start with these topics in order:
            a. "Introduction to {course_title}" – broad introduction to the course.  
            b. "Overview – {course_title}" – short, clear summary without examples or code.  
            c. "Learning Objectives – {course_title}" – numbered list of at least {real_learning_obj} objectives.  
                - Objective 5 must combine Objectives 1–4 into one integrative objective.

            2. Immediately after "Learning Objectives – {course_title}", the first topic title must match Learning Objective #1, with the description expanding on it. Continue sequentially for all objectives.

            3. For each topic:
           - The "description" must **strictly and completely match every word, phrase, and item in the learning objective title**. It must fully expand each part with clear definitions, detailed explanations, multiple examples, practical applications, and, where relevant, comparisons. No element from the title may be skipped or only partially covered.
                (Example: If the title is "Explain and apply data types, variables, and operators in Python," the description must include and explain all three parts: data types, variables, and operators, not just one or two of them.)  
            - Write "description" as **lesson-style text** with definition, explanations, examples, and applications.  
            - Always use **double backslashes for newlines** (`\\n`).  
            - Escape all double quotes inside strings as `\"`.  
            - Include **at least 5 runnable code examples** (if relevant), formatted properly, each with **line-by-line comments**.  
            - Provide **solutions** for exercises or challenges.  
            - Include **real-world examples** where this concept applies.  
            - End each topic with a **mini-project or small assignment**, explained step by step.

            4. Python lessons:
            - Always format code exactly as:
                ```python
                def sample_function():
                    return "Example"  # This function returns the string "Example"

                print(sample_function())  # This line prints the result of the function
                ```
            - Every line of code must have a **comment below it**, explaining what it does.

            5. HTML or web-related lessons:
            - The "description" field must **never contain raw HTML tags**.  
            - Detect and **escape all HTML tags** (`<div>` → `&lt;div&gt;`).  
            - Only include the **full HTML structure** (`&lt;!DOCTYPE html&gt; ... &lt;/html&gt;`) if the lesson requires a complete page.  
            - Otherwise, show just the snippet wrapped inside:
                <pre><code class="language-html"> ... </code></pre>

            6. Output format:
            - A single valid **JSON array** of {num_topics} objects.  
            - Each object must have exactly 2 keys:  
                - "title"  
                - "description"  
            - Do not include any extra text outside the JSON.  
            - Always escape special characters:  
                - Newlines → `\\n`  
                - Double quotes → `\"`  
                - Tabs → `\\t`

        # RULES:
        # Always start with these topics in order:
        # 1. "Introduction to {course_title}"
        # 2. "Overview – {course_title}" – short, clear summary without examples or code.
        # 3. "Learning Objectives – {course_title}" – numbered list of at least {real_learning_obj} objectives. Objective 5 must combine Objectives 1-4 into one integrative objective.
        # 4. Immediately after "Learning Objectives – {course_title}", the first topic title must match Learning Objective #1, with description expanding on it. Continue sequentially for all objectives.
        # 5. For each topic:
        # - Provide a detailed explanation of the concept based on the learning objectives.
        # - Include at least 5 runnable code examples demonstrating practical usage with addintional comments side by side.
        # - Provide solutions for any exercises or challenges mentioned.
        # - Each learning objective title must be expanded into a clear and detailed description that fully explains the concept.
        # - Give real-world examples showing where this concept is applied based on the topics on the next line.
        # - Explain and demostrate the mini-project or the small practical assignment.
        # 6. if the codes is python, follow these rules strictly and make sure you add comments below each code:
        #     ```python
        #     def explain_python(): 
        #         return 'Python is widely used in AI due to its simplicity.'
        #     print(explain_python())
        #     ```
        # 7. If the course is HTML or web-related:
        #     * The "description" field must **never contain raw HTML tags**. 
        #     * Detect **any HTML tag** (headings, links, lists, divs, spans, images, etc.) and always escape them as `&lt;` and `&gt;`.
        #     * This applies everywhere: in normal text, explanations, examples, inline mentions, and pitfalls.
        #     * Only include the **full HTML structure** (`&lt;!DOCTYPE html&gt; ... &lt;/html&gt;`) if the lesson specifically requires a complete page.
        #     * Otherwise, show just the snippet in `<pre><code class="language-html">...</code></pre>`.

        # 8. Output: single valid JSON array of {num_topics} objects with keys "title" and "description" only. Use \\n for line breaks in descriptions. make sure the description is details based on the title.
        # """
        else:
            prompt += f"""
        RULES:
        1. Always start with these topics in order:
        1. "Introduction to {course_title}"
        2. "Overview – {course_title}" – short, clear summary without examples or code.
        3. "Learning Objectives – {course_title}" – numbered list of at least {real_learning_obj} objectives. Objective 5 must combine Objectives 1-4 into one integrative objective. Conclude with a summary paragraph.
        4. Immediately after "Learning Objectives – {course_title}", the first topic title must match Learning Objective #1, with description expanding on it. Continue sequentially for all objectives.
        2. Generate topics with exactly 5 paragraphs per description:
        - Paragraphs must be substantial, coherent, and instructor-ready.
        - The first paragraph must open with a learner-centered hook.
        - One paragraph must contain a numbered bullet-point list with at least 4 items.
        - Include at least one real-life teaching story using Setup, Challenge, Action, Outcome, Lesson learned.
        3. Output: single valid JSON array of {num_topics} objects with keys "title" and "description" only, separated by \\n.
        """

        def clean_response(text):
            if text.startswith("```"):
                text = text.strip("`")
                text = text.lstrip("json").strip()
            import re
            match = re.search(r"(\[.*\])", text, re.DOTALL)
            if match:
                return match.group(1).strip()
            return text.strip()

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=4000,
                    temperature=0
                )

                if not response.choices:
                    messages.error(request, "OpenAI returned no content.")
                    return redirect('quiz:ai_topics_generator')

                topics_text = response.choices[0].message.content.strip()
                topics_text = clean_response(topics_text)

                topics_json = json.loads(topics_text)
                break  # Success

            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    messages.error(request, f"Failed to parse AI JSON output after {max_retries} attempts. Error: {e}")
                    return redirect('quiz:ai_topics_generator')
            except Exception as e:
                messages.error(request, f"OpenAI error: {str(e)}")
                return redirect('quiz:ai_topics_generator')

        preview_topics = []
        heading_keywords = ["include:", "are:", "must:", "consist of:", "types of", "principles of"]

        import html 

        for topic in topics_json:
            description = topic.get("description", "")
            lines = description.split("\n")

            formatted_lines = []
            in_code_block = False
            current_lang = ""

            for line in lines:
                stripped = line.strip()

                # Fenced code block start
                if stripped.startswith("```") and not in_code_block:
                    in_code_block = True
                    current_lang = stripped.replace("```", "").strip().lower()
                    lang_class = f' class="language-{current_lang}"' if current_lang else ""
                    formatted_lines.append(f"<pre><code{lang_class}>")
                    continue

                # Fenced code block end
                elif stripped.startswith("```") and in_code_block:
                    in_code_block = False
                    current_lang = ""
                    formatted_lines.append("</code></pre>")
                    continue

                # Already wrapped <pre><code> from AI output
                elif stripped.startswith("<pre><code"):
                    in_code_block = True
                    formatted_lines.append(stripped)
                    continue

                elif stripped.startswith("</code></pre>"):
                    in_code_block = False
                    formatted_lines.append(stripped)
                    continue

                # Inside *any* code block → escape HTML
                if in_code_block:
                    formatted_lines.append(html.escape(line))

                else:
                    # Outside code blocks → escape ALL tags first
                    safe_line = html.escape(stripped)

                    # Then apply formatting rules
                    if any(keyword.lower() in stripped.lower() for keyword in heading_keywords):
                        formatted_lines.append(f"<h3>{safe_line}</h3>")
                    elif stripped:
                        formatted_lines.append(f"<p>{safe_line}</p>")

            formatted_desc = "\n".join(formatted_lines)

            preview_topics.append({
                    "title": topic.get("title", ""),
                    "desc": formatted_desc,
                    "transcript": ""
                })


        return render(request, 'quiz/dashboard/ai_topics_generator.html', {
            'categories': categories,
            'courses': courses,
            'preview_topics': preview_topics,
            'category_id': category_id,
            'course_id': course_id,
            'num_objectives': len(objectives_list) if custom_objectives else 5,  # default
        })

    # GET request
    return render(request, 'quiz/dashboard/ai_topics_generator.html', {
        'categories': categories,
        'courses': courses,
        'num_objectives': 5,  # default for GET
    })




def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def ai_assessment_selector(request):
    # URLs and display names
    options = [
        {'name': 'AI Summative Assessment', 'url': reverse('quiz:ai_summative_assessment')},
        {'name': 'AI formative assessment', 'url': reverse('quiz:generate_ai_questions')},
        {'name': 'AI Topic Generator', 'url': reverse('quiz:ai_topics_generator')},
        ai_topics_generator
    ]

    if request.method == 'POST':
        selected_url = request.POST.get('selected_option')
        if selected_url:
            return redirect(selected_url)

    return render(request, 'quiz/dashboard/ai_assessment_selector.html', {'options': options})


@login_required
def ai_summative_assessment(request):
    courses = Courses.objects.all()  # List all courses for selection

    if request.method == 'POST' and request.POST.get("confirm_save") == "1":
        total_questions = int(request.POST.get("total_questions", 0))
        course_id = request.POST.get("course_id")
        marks = int(request.POST.get("marks", 1))

        try:
            course_obj = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            messages.error(request, "Invalid course selected.")
            return redirect('quiz:ai_summative_assessment')

        # Find a related CourseDetail (Course) instance to assign to Question
        course_detail = Course.objects.filter(course_name=course_obj).first()
        if not course_detail:
            messages.error(request, "No course details found for the selected course.")
            return redirect('quiz:ai_summative_assessment')

        saved = 0
        for i in range(1, total_questions + 1):
            question_text = request.POST.get(f"question_{i}", "").strip()
            option1 = request.POST.get(f"option1_{i}", "").strip()
            option2 = request.POST.get(f"option2_{i}", "").strip()
            option3 = request.POST.get(f"option3_{i}", "").strip()
            option4 = request.POST.get(f"option4_{i}", "").strip()
            answer = request.POST.get(f"answer_{i}", "Option1").strip()

            if question_text and option1 and option2 and option3 and option4:
                Question.objects.create(
                    course=course_detail,  # Assign CourseDetail instance
                    marks=marks,
                    question=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    answer=answer
                )
                saved += 1

        messages.success(request, f"{saved} questions saved successfully.")
        return redirect('quiz:ai_summative_assessment')

    elif request.method == 'POST':
        course_id = request.POST.get('course')
        num_questions = int(request.POST.get('num_questions', 5))
        marks = int(request.POST.get('marks', 1))
        difficulty = request.POST.get('difficulty', 'medium').lower()

        try:
            course_obj = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            messages.error(request, "Invalid course selected.")
            return redirect('quiz:ai_summative_assessment')

        course_title = course_obj.title or ""

        # Decide subject_tag for prompt if you want
        subject_tag = course_title.split()[0].lower() if course_title else ""

        # Get related CourseDetail
        course_detail = Course.objects.filter(course_name=course_obj).first()
        if not course_detail:
            messages.error(request, "No course details found for this course. assign it to a course.")
            return redirect('quiz:ai_summative_assessment')

        if subject_tag in ['maths', 'mathematics', 'math', 'chemistry', 'chem', 'physics']:
            prompt = f"""

                You are an expert in learning assessment.

                Generate {num_questions} {difficulty}-level multiple-choice questions based strictly on the topic '{topic_title}'. 
                Questions must follow Bloom's Taxonomy and include at least one question from each relevant category for the selected difficulty:

                - Easy: Remembering, Understanding
                - Medium: Remembering, Understanding, Applying, Analyzing
                - Hard: Remembering, Understanding, Applying, Analyzing, Evaluating, Creating

                Each question must directly test knowledge, comprehension, application, analysis, evaluation, or creation related to '{topic_title}' using accurate and realistic information.

                Strictly follow this format (no explanations, no extra text, no numbering):

                Question: <math xmlns='http://www.w3.org/1998/Math/MathML'><mfrac><msup><mn>3</mn><mn>4</mn></msup><msup><mn>3</mn><mn>2</mn></msup></mfrac></math>?

                A. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>9</mn></math>  
                B. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>6</mn></math>  
                C. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>3</mn></math>  
                D. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>27</mn></math>  
                Answer: A

                Rules:
                1. Randomize the correct answer position for each question.
                2. Avoid repeating options, reusing the same distractors, or duplicating questions.
                3. Keep wording clear, concise, and unambiguous.
                4. Ensure at least one question per relevant Bloom's category for the chosen difficulty level.
                5. Make questions challenging but fair, using context or examples related to '{course_title}'.
                """
        else:
            prompt = f"""

            You are an expert in learning assessment.

            Generate {num_questions} {difficulty}-level multiple-choice questions based strictly on the topic '{course_title}'. 
            Questions must follow Bloom's Taxonomy and include at least one question from each relevant category for the selected difficulty:

            - Easy: Remembering, Understanding
            - Medium: Remembering, Understanding, Applying, Analyzing
            - Hard: Remembering, Understanding, Applying, Analyzing, Evaluating, Creating

            Each question must directly test knowledge, comprehension, application, analysis, evaluation, or creation related to '{course_title}' using accurate and realistic information.

            Strictly follow this format (no explanations, no extra text, no numbering):

            Question: <question text>
            A. <option>
            B. <option>
            C. <option>
            D. <option>
            Answer: <correct option letter>

            Rules:
            1. Randomize the correct answer position for each question.
            2. Avoid repeating options, reusing the same distractors, or duplicating questions.
            3. Keep wording clear, concise, and unambiguous.
            4. Ensure at least one question per relevant Bloom's category for the chosen difficulty level.
            5. Make questions challenging but fair, using context or examples related to '{course_title}'.
            """
            

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates professional learning quiz questions."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=6000,
                temperature=0,
            )

            if not response.choices:
                messages.error(request, "OpenAI returned no content.")
                return redirect('quiz:ai_summative_assessment')

            questions_text = response.choices[0].message.content.strip()
            blocks = re.split(r'\n\s*\n', questions_text.strip())

            preview_questions = []
            skipped_blocks = 0
            for block in blocks:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) == 6:
                    question_text = lines[0].replace("Question:", "").strip()
                    options = [line.split('. ', 1)[1].strip() for line in lines[1:5]]
                    answer_letter = lines[5].split(':')[-1].strip().upper()

                    answer_map = {'A': 'Option1', 'B': 'Option2', 'C': 'Option3', 'D': 'Option4'}
                    answer = answer_map.get(answer_letter, 'Option1')

                    preview_questions.append({
                        'question': question_text,
                        'option1': options[0],
                        'option2': options[1],
                        'option3': options[2],
                        'option4': options[3],
                        'answer': answer
                    })
                else:
                    skipped_blocks += 1

            if skipped_blocks > 0:
                messages.warning(request, f"Skipped {skipped_blocks} malformed question blocks from AI response.")

            return render(request, 'quiz/dashboard/ai_summative_assessment.html', {
                'courses': courses,
                'preview_questions': preview_questions,
                'course_id': course_id,
                'marks': marks,
            })

        except Exception as e:
            messages.error(request, f"OpenAI error: {str(e)}")
            return redirect('quiz:ai_summative_assessment')

    # GET request
    return render(request, 'quiz/dashboard/ai_summative_assessment.html', {
        'courses': courses
    })




@login_required
def generate_ai_questions(request):
    assessments = TopicsAssessment.objects.select_related('course_name').all()

    # ✅ Handle confirm-save POST request
    if request.method == 'POST' and request.POST.get("confirm_save") == "1":
        total_questions = int(request.POST.get("total_questions"))
        assessment_id = request.POST.get("assessment_id")
        marks = int(request.POST.get("marks"))

        try:
            assessment = TopicsAssessment.objects.get(id=assessment_id)
        except TopicsAssessment.DoesNotExist:
            messages.error(request, "Invalid assessment.")
            return redirect('quiz:generate_ai_questions')

        saved = 0
        for i in range(1, total_questions + 1):
            question_text = request.POST.get(f"question_{i}", "").strip()
            option1 = request.POST.get(f"option1_{i}", "").strip()
            option2 = request.POST.get(f"option2_{i}", "").strip()
            option3 = request.POST.get(f"option3_{i}", "").strip()
            option4 = request.POST.get(f"option4_{i}", "").strip()
            answer = request.POST.get(f"answer_{i}", "Option1").strip()

            if question_text and option1 and option2 and option3 and option4:
                QuestionAssessment.objects.create(
                    course=assessment,
                    marks=marks,
                    question=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    answer=answer
                )
                saved += 1

        messages.success(request, f"{saved} edited questions saved successfully.")
        return redirect('quiz:generate_ai_questions')

    # ✅ Initial generation POST request
    elif request.method == 'POST':
        assessment_id = request.POST.get('assessment')
        num_questions = int(request.POST.get('num_questions', 5))
        marks = int(request.POST.get('marks', 1))
        difficulty = request.POST.get('difficulty', 'medium').lower()  # 🔹 Read difficulty from form
        # print("🛠 DEBUG — Selected difficulty:", difficulty)  # <-- Debug line

        try:
            assessment = TopicsAssessment.objects.get(id=assessment_id)
        except TopicsAssessment.DoesNotExist:
            messages.error(request, "Invalid assessment selected.")
            return redirect('quiz:generate_ai_questions')

        topic_title = assessment.course_name.courses.title

        def extract_subject_tag(topic_title):
            """Extracts the subject from a string like 'MATHS JSS2'."""
            return topic_title.split()[0].lower()

        subject_tag = extract_subject_tag(topic_title)
        topics = assessment.course_name

        # 🔹 Inject difficulty into the AI prompt
        if subject_tag in ['maths', 'mathematics', 'math', 'chemistry', 'chem', 'physics']:
            prompt = f"""Generate {num_questions} multiple-choice questions on the topic '{topics}' 
            at a {difficulty} difficulty level.
            Each question and its options must be strictly formatted using MathML with the namespace
            http://www.w3.org/1998/Math/MathML.

            Question: <math xmlns='http://www.w3.org/1998/Math/MathML'><mfrac><msup><mn>3</mn><mn>4</mn></msup><msup><mn>3</mn><mn>2</mn></msup></mfrac></math>?
            A. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>9</mn></math>
            B. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>6</mn></math>
            C. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>3</mn></math>
            D. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>27</mn></math>
            Answer: A
            """
        else:
           prompt = f"""
            You are an expert in learning assessment.

            Generate {num_questions} {difficulty}-level multiple-choice questions based strictly on the topic '{topic_title}'. 
            Questions must follow Bloom's Taxonomy and include at least one question from each relevant category for the selected difficulty:

            - Easy: Remembering, Understanding
            - Medium: Remembering, Understanding, Applying, Analyzing
            - Hard: Remembering, Understanding, Applying, Analyzing, Evaluating, Creating

            Each question must directly test knowledge, comprehension, application, analysis, evaluation, or creation related to '{topic_title}' using accurate and realistic information.

            Strictly follow this format (no explanations, no extra text, no numbering):

            Question: <question text>
            A. <option>
            B. <option>
            C. <option>
            D. <option>
            Answer: <correct option letter>

            Rules:
            1. Randomize the correct answer position for each question.
            2. Avoid repeating options, reusing the same distractors, or duplicating questions.
            3. Keep wording clear, concise, and unambiguous.
            4. Ensure at least one question per relevant Bloom's category for the chosen difficulty level.
            5. Make questions challenging but fair, using context or examples related to '{topic_title}'.
            """
           
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates programming quiz questions."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=6000,
                temperature=0,
            )

            if not response.choices:
                messages.error(request, "OpenAI returned no content.")
                return redirect('quiz:generate_ai_questions')

            questions_text = response.choices[0].message.content.strip()
            blocks = re.split(r'\n\s*\n', questions_text.strip())

            preview_questions = []
            for block in blocks:
                lines = block.strip().split("\n")
                if len(lines) == 6:
                    question_text = lines[0].replace("Question:", "").strip()
                    options = [line.split('. ', 1)[1].strip() for line in lines[1:5]]
                    answer_letter = lines[5].split(':')[-1].strip().upper()

                    answer_map = {'A': 'Option1', 'B': 'Option2', 'C': 'Option3', 'D': 'Option4'}
                    answer = answer_map.get(answer_letter, 'Option1')

                    preview_questions.append({
                        'question': question_text,
                        'option1': options[0],
                        'option2': options[1],
                        'option3': options[2],
                        'option4': options[3],
                        'answer': answer
                    })
                else:
                    messages.warning(request, f"⚠️ Skipped malformed block:\n{block[:60]}...")

            return render(request, 'quiz/dashboard/generate_questions.html', {
                'assessments': assessments,
                'preview_questions': preview_questions,
                'assessment_id': assessment_id,
                'marks': marks,
            })

        except Exception as e:
            messages.error(request, f"OpenAI error: {str(e)}")
            return redirect('quiz:generate_ai_questions')

    # GET request
    return render(request, 'quiz/dashboard/generate_questions.html', {
        'assessments': assessments
    })




@login_required
def take_exams_view(request):
    course = TopicsAssessment.objects.get_queryset().order_by('id')
    # print("Course Title:", course.title)
    for ta in TopicsAssessment.objects.all():
        print("TopicsAssessment Course Name Title:", ta.course_name.title)
        print("TopicsAssessment topic Name:", ta.course_name)
    context = {
        'courses':course,
        'courses_title':ta.course_name.title,
        'courses_name':ta.course_name
    }
    return render(request, 'quiz/dashboard/take_exams.html', context=context)

from sms.models import Categories, Topics, Courses
from django.shortcuts import redirect, render, get_object_or_404
from urllib.parse import unquote
from string import ascii_uppercase  # Import uppercase letters



from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse



@login_required
def start_exams_view(request, pk):
    
    course = TopicsAssessment.objects.get(id = pk)
    questions = QuestionAssessment.objects.filter(course = course).order_by('id')
    topics = Topics.objects.all()
    q_count = QuestionAssessment.objects.all().filter(course = course).count()
    student = request.user.profile
    results = ResultAssessment.objects.filter(exam = course, student = student).order_by('id')
    paginator = Paginator(questions, 1000) # Show 25 contacts per page.
    paginator_comp = Paginator(questions, 1) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
   
    page_obj_comp = paginator_comp.get_page(page_number)
    letters = list(ascii_uppercase)

    context = {
        'course':course,
        'questions':questions,
        'q_count':q_count,
        'page_obj':page_obj,
        'page_obj_comp':page_obj_comp,
        'results':results,
        'letters':letters,
        'completed':"letters",
      
    }
    if request.method == 'POST':
        pass
    response = render(request, 'quiz/dashboard/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response
     
# end of dashboard view


from django.urls import reverse

@login_required
def calculate_marks_assessment(request):
    if request.COOKIES.get('course_id'):
        course_id = request.COOKIES.get('course_id')
        course = get_object_or_404(TopicsAssessment, id=course_id)
        questions = QuestionAssessment.objects.filter(course=course).order_by('id')
        
        total_marks = 0
        selected_options = {}  # Store answers keyed by question id
        
        for q in questions:
            selected_option = request.POST.get(str(q.id))
            selected_options[str(q.id)] = selected_option
            
            # Compare safely
            if selected_option and selected_option.strip() == q.answer.strip():
                total_marks += q.marks

        student = get_object_or_404(Profile, user_id=request.user.id)

        # Check if result exists
        result, created = ResultAssessment.objects.get_or_create(
            exam=course,
            student=student,
            defaults={'marks': total_marks, 'option': selected_options}
        )

        if not created:
            # Update existing result
            result.marks = total_marks
            result.option = selected_options
            result.save()

        return redirect(reverse('quiz:start-exam', kwargs={'pk': course.pk}))
    else:
        return HttpResponseRedirect('quiz:take-exam')


# @login_required
# def calculate_marks_view(request):
#     if request.COOKIES.get('course_id') is not None:
#         course_id = request.COOKIES.get('course_id')
#         course= TopicsAssessment.objects.get(id=course_id)
#         options = []  # List to store the selected options
#         total_marks=0
#         questions= QuestionAssessment.objects.get_queryset().filter(course=course).order_by('id')
#         for i in range(len(questions)):
            
#             # selected_ans = request.COOKIES.get(str(i+1))
#             selected_ans = request.POST.get(str(i+1))
#             options.append(selected_ans)  # Add selected option to the list
#             print("answers", selected_ans)
            
#             actual_answer = questions[i].answer
#             if selected_ans == actual_answer:
#                 total_marks = total_marks + questions[i].marks
#         student = Profile.objects.get(user_id=request.user.id)
        
#         result =ResultAssessment()
        
#         result.marks=total_marks 
#         result.exam=course
#         result.student=student
#         # options_str = ", ".join(str(option) if option is not None else "None" for option in options)
#         result.option = options  # Save selected options as a comma-separated string
        
#         print("result", result)
#         print("pass mar", course.pass_mark)
        
#         result.save()

#         return HttpResponseRedirect(reverse('quiz:start-exam', kwargs={'pk': course.pk}))
#     else:
#         return HttpResponseRedirect('take-exam')



@login_required
def view_result_view(request):
    courses= TopicsAssessment.objects.get_queryset().order_by('id')
    return render(request,'quiz/dashboard/view_result.html',{'courses':courses})


from django.db.models import Count

@login_required
def check_marks_view(request,pk):
    course= TopicsAssessment.objects.get(id=pk)
    student = Profile.objects.get_queryset().order_by('id')
 
    context = {
        'results':student,
        'course':course,
        'st':request.user,
        
    }
    return render(request,'quiz/dashboard/check_marks.html', context)


# end

# views.py

from django.shortcuts import render, redirect
# from .forms import StudentRegistrationForm

# def register_student(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('quiz:school_dashboard')
#     else:
#         form = StudentRegistrationForm()

#     return render(request, 'quiz/dashboard/student_registration.html', {'form': form})


# def school_dashboard(request, pk):

#         # Example usage (in a view or wherever you generate the certificate)
#     course = Course.objects.get(pk=pk)  # Replace with the actual course instance
#     student = Student.objects.get(pk=pk)  # Replace with the actual student instance
#     # Get the relevant information for the certificate
#     student_info = course.get_student_info_for_certificate(student)

#     # Now you can use student_info in your certificate generation logic
#     if student_info:
#         school_name = student_info['school_name']
#         logo_url = student_info['logo_url']
#         signature_url = student_info['signature_url']
#         # Add more fields as needed
 
#     context = {
#         'course': course,
#         'student': student,
#         'student_info': student_info,
#     }
#     # context =  {
#     #     'school_name': school_name,
#     #     'logo_url': logo_url,
#     #     'signature_url': signature_url,
#     #     }

#     return render(request, 'quiz/dashboard/school_dashboard.html', context)
# from django.shortcuts import render
# from .models import Course
# from .models import Student

# from .models import Student

# def get_student_for_user(user):
#     try:
#         # Assuming there is a one-to-one relationship between User and Student
#         return Student.objects.get(user=user.profile)
#     except Student.DoesNotExist:
#         return None


# def school_dashboard(request, course_id):
#     # Assuming you have a function to get the current student based on the logged-in user
#     student = get_student_for_user(request.user)

#     if student:
#         course = get_object_or_404(Course, id=course_id)

#         # Get the relevant information for the certificate
#         student_info = course.get_student_info_for_certificate(student)

#         # Pass the information to the template
#         context = {
#             'course': course,
#             'student': student,
#             'student_info': student_info,
#         }

#         return render(request, 'quiz/dashboard/school_dashboard.html', context)
#     else:
#         # Handle the case where the user is not associated with a student
#         return render(request, 'error_template.html', {'error_message': 'User is not associated with a student'})
