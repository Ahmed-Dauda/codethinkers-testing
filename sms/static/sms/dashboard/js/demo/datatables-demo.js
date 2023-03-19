// Call the dataTables jQuery plugin
// $(document).ready(function() {
//   $('#dataTable').DataTable();
// });

$(document).ready(function() {
  $('#dataTable').dataTable( {
      "lengthMenu": [[1, 2, 3, -1], [1, 2, 3, "All"]],
    
  } );
} )