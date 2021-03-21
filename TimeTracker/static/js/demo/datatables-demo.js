// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({paging:false});
  $('#chargeCodeTable').DataTable({paging:true});
  $('#chargeCodeToday').DataTable({ paging: false });
});
