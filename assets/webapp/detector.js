$("#submit").on("click", function () {
  console.log(uppy.getFiles());

  csrftoken = $('input[name=csrfmiddlewaretoken]').val();

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  if (uppy.getFiles()['length'] > 0) {
    $.ajax({
      type: 'POST',
      url: '/checkICH',
      data: {
        image: uppy.getFiles()[0]["tus"]["uploadUrl"],
        name: uppy.getFiles()[0]["name"],
        action: 'post'
      },
      success: function (json) {
        console.log(json)
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