$("#submit").on("click", function () {
  console.log(uppy.getFiles());
  // var link = document.createElement('a');
  // link.href = uppy.getFiles()[0]["preview"];
  // link.download = uppy.getFiles()[0]["name"];
  // document.body.appendChild(link);
  // link.click();
  // document.body.removeChild(link);
  if (uppy.getFiles()['length'] > 0) {
    $.ajax({
      type: 'POST',
      url: '/checkICH',
      data: {
        image: uppy.getFiles()[0]["preview"],
        name: uppy.getFiles()[0]["name"],
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function (json) {
        alert("submitted")
      },
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  }
  else {
    alert("Upload at least one image");
  }
});