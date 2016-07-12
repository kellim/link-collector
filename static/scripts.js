// Submit form when collection is chosen from dropdown list in sidebar
$("#select-coll").change(function() {
  $("#frm-select-coll").submit();
});

var url = window.location.href;

// If user is authorized to delete selected collection,
// open modal after user clicks delete collection.
// Currently only admins can delete collections.
if (url.search("_del-coll") >= 0) {
  $.getJSON($SCRIPT_ROOT+"/_auth-to-del", function(r){
    if (r.is_auth_to_delete) {
      $('#collectiondelete').modal('toggle');
    }
  });
}

// If user is authorized to delete selected link,
// open modal after user clicks delete link
if (url.search("_del-link") >= 0) {
  var link = url.substr(url.indexOf('/_del-link/') + 11);
  $.getJSON($SCRIPT_ROOT+"/_auth-to-del",
    {
        link: link
    },
    function(data) {
      if (data.is_auth_to_delete) {
        $('#linkdelete').modal('toggle');
    }
  });
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