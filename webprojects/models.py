from django.db import models
from sms.models import Courses, Topics, Categories
from users.models import NewUser as User
from cloudinary.models import CloudinaryField
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Window, F
from django.db.models.functions import Rank
from sms.models import Courses, Topics
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Window, F
from django.db.models.functions import Rank
from sms.models import Courses, Topics

User = get_user_model()


# ---------------- Project ----------------

class Project(models.Model):
    name   = models.CharField(max_length=100)
    course = models.ForeignKey(
        'sms.Courses',            # ← explicit app.Model string avoids mis-resolution
        on_delete=models.CASCADE,
        null=True,
        related_name="projects"
    )
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/webprojects/{self.id}/"

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


# ---------------- Folder ----------------
class Folder(models.Model):
    project = models.ForeignKey(Project, related_name="folders", on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)
    parent  = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    topic   = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        parent_name = f" > {self.parent.name}" if self.parent else ""
        return f"{self.name}{parent_name} (Folder ID: {self.id})"


# ---------------- File ----------------
class File(models.Model):

    current_topic = models.ForeignKey(
        'sms.Topics',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_files',
        help_text="Which lesson is this file for?"
    )
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        default=None,
        related_name="files",
        on_delete=models.CASCADE
    )
    folder = models.ForeignKey(
        Folder,
        null=True,
        blank=True,
        related_name="files",
        on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_files"
    )

    name    = models.CharField(max_length=300)
    content = models.TextField(blank=True)

    image = CloudinaryField('image', blank=True, null=True)
    file  = models.FileField(upload_to='uploads/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (File ID: {self.id}) — Project: {self.project.name}"

    def extension(self):
        return self.name.split('.')[-1].lower()

    def is_python(self):  return self.name.lower().endswith(".py")
    def is_css(self):     return self.extension() == "css"
    def is_js(self):      return self.extension() == "js"
    def is_html(self):    return self.extension() in ["html", "htm"]
    def is_image(self):   return self.extension() in ["jpg", "jpeg", "png", "gif", "svg", "webp"]
    def is_excel(self):   return self.extension() in ["xls", "xlsx", "csv"]

    def file_url(self):
        if self.image: return self.image.url
        if self.file:  return self.file.url
        return ""

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Window, F
from django.db.models.functions import Rank
from django.utils import timezone
from sms.models import Courses, Topics

User = get_user_model()


# ============================================
# STUDENT XP (GLOBAL)
# ============================================

class StudentXP(models.Model):
    """Global XP tracking across all courses"""
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='xp_profile')
    total_xp = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Student XP'
        verbose_name_plural = 'Student XP'
    
    def __str__(self):
        return f"{self.student.username} — {self.total_xp}XP"
    
    def add_xp(self, amount):
        """Add XP and update total"""
        self.total_xp += amount
        self.save(update_fields=['total_xp'])


# ============================================
# STUDENT PROGRESS (PER COURSE)
# ============================================

class StudentProgress(models.Model):
    """Tracks student progress through a course"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='student_progress')
    completed_topics = models.ManyToManyField(
        Topics, 
        blank=True, 
        related_name='completed_by_students'
    )
    current_topic = models.ForeignKey(
        Topics, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='current_for_students'
    )
    
    # Assessment tracking
    assessment_scores = models.JSONField(default=list)
    total_assessments_taken = models.IntegerField(default=0)
    
    # Code challenge tracking
    coding_challenges_passed = models.IntegerField(default=0)
    incorrect_code_attempts = models.IntegerField(default=0)
    
    # Learning streaks
    last_activity_date = models.DateField(null=True, blank=True)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    
    # Completion tracking
    course_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    first_to_complete = models.BooleanField(default=False)
    
    # Assessment attempt tracking
    first_attempt_topics = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-last_updated']
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress'
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['course', '-current_streak']),
        ]
    
    def __str__(self):
        return f"{self.student.username} — {self.course.title}"
    
    def get_average_score(self):
        """Calculate average assessment score"""
        if not self.assessment_scores:
            return 0.0
        return round(sum(self.assessment_scores) / len(self.assessment_scores), 1)
    
    def add_assessment_score(self, score, topic_id, first_attempt=False):
        """Add an assessment score and track first attempts"""
        if not isinstance(self.assessment_scores, list):
            self.assessment_scores = []
        self.assessment_scores.append(score)
        self.total_assessments_taken += 1
        
        if first_attempt and topic_id not in self.first_attempt_topics:
            if not isinstance(self.first_attempt_topics, list):
                self.first_attempt_topics = []
            self.first_attempt_topics.append(topic_id)
        
        self.save(update_fields=['assessment_scores', 'total_assessments_taken', 'first_attempt_topics'])
    
    def get_completion_percentage(self, total_topics):
        """Get completion percentage capped at 100"""
        if total_topics == 0:
            return 0.0
        completed = self.completed_topics.count()
        return min(round((completed / total_topics) * 100, 1), 100.0)


# ============================================
# BADGES
# ============================================

class Badge(models.Model):
    """Badges that can be earned"""
    BADGE_TYPES = [
        ('first_to_finish', '🥇 First to Finish'),
        ('fast_learner', '⚡ Fast Learner'),
        ('perfect_score', '🎯 Perfect Score'),
        ('code_master', '💻 Code Master'),
        ('ai_champion', '🧠 AI Champion'),
        ('consistent', '🔥 Consistent Learner'),
    ]
    
    name = models.CharField(max_length=50, choices=BADGE_TYPES, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    xp_reward = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
    
    def __str__(self):
        return self.get_name_display()


class StudentBadge(models.Model):
    """Badges earned by students"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_to')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True, blank=True, related_name='badges_awarded')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'badge', 'course']
        ordering = ['-earned_at']
        verbose_name = 'Student Badge'
        verbose_name_plural = 'Student Badges'
    
    def __str__(self):
        return f"{self.student.username} — {self.badge.get_name_display()}"


# ============================================
# LEARNING STREAKS
# ============================================

class LearningStreak(models.Model):
    """Tracks daily learning streaks"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_streaks')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True, blank=True, related_name='student_streaks')
    date = models.DateField()
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']
        verbose_name = 'Learning Streak'
        verbose_name_plural = 'Learning Streaks'
        indexes = [
            models.Index(fields=['student', 'course', '-date']),
        ]
    
    def __str__(self):
        return f"{self.student.username} — {self.date}"


# ============================================
# LEADERBOARD
# ============================================

class LeaderboardEntry(models.Model):
    """Course leaderboard with Champion XP system"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='leaderboard')
    
    # Champion XP
    champion_xp = models.IntegerField(default=0)
    
    # Stats
    modules_completed = models.IntegerField(default=0)
    total_modules = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    coding_challenges_passed = models.IntegerField(default=0)
    incorrect_code_attempts = models.IntegerField(default=0)
    completion_time_days = models.IntegerField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    learning_streak = models.IntegerField(default=0)
    
    # Rank
    rank = models.IntegerField(null=True, blank=True)
    
    # Timestamp
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['rank']
        verbose_name = 'Leaderboard Entry'
        verbose_name_plural = 'Leaderboard Entries'
        indexes = [
            models.Index(fields=['course', 'rank']),
            models.Index(fields=['course', '-champion_xp']),
        ]
    
    def __str__(self):
        return f"{self.student.username} — {self.course.title} (Rank #{self.rank})"
    
    def update_rank(self):
        """Update ranks for all entries in this course with proper tie handling"""
        entries = LeaderboardEntry.objects.filter(course=self.course).annotate(
            calculated_rank=Window(
                expression=Rank(),
                order_by=[
                    F('champion_xp').desc(),
                    F('average_score').desc(),
                    F('incorrect_code_attempts').asc(),
                    F('completion_time_days').asc(nulls_last=True),
                    F('completion_date').asc(nulls_last=True),
                ]
            )
        )
        
        for entry in entries:
            if entry.rank != entry.calculated_rank:
                entry.rank = entry.calculated_rank
                entry.save(update_fields=['rank'])
    
    def save(self, *args, **kwargs):
        """Auto-cap values on save"""
        if self.total_modules > 0:
            if self.modules_completed > self.total_modules:
                self.modules_completed = self.total_modules
        super().save(*args, **kwargs)