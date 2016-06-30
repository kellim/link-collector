// Submit form when collection is chosen from dropdown list in sidebar
$("#select-coll").change(function() {
  $("#frm-select-coll").submit();
});

var url = window.location.href;

// Open modal after user clicks delete collection
if (url.search("_del-coll") >= 0) {
    $('#collectiondelete').modal('toggle');
}

// Open modal after user clicks delete link
if (url.search("_del-link") >= 0) {
    $('#linkdelete').modal('toggle');
}

// When the collection delete modal closes, go back to main
// index url instead of _delete/<collection> url.
$('#collectiondelete').on('hidden.bs.modal', function () {
  window.location.replace("../");
})

// When the link delete modal closes, go back to
// category/links page instead of _delete/<collection> url.
$('#linkdelete').on('hidden.bs.modal', function () {
  window.location.replace("../");
})