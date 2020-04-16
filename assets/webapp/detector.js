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
  files = uppy.getFiles()
  if (files['length'] > 0) {
    imageURL = files[0]["tus"]["uploadUrl"]
    imageName = files[0]["name"]
    for (i = 1; i<files['length']; i++){
      imageURL += "~" + files[i]["tus"]["uploadUrl"]
      imageName += "~" + files[i]["name"]
    }
    $.ajax({
      type: 'POST',
      url: '/checkICH',
      data: {
        image: imageURL,
        name: imageName,
        action: 'post'
      },
      success: function (json) {
        window.location = "/results";
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