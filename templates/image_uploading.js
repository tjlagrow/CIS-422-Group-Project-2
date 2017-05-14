
    $('#page').on('pageinit', function(){
    $("#chooseFile").click(function(e){
      e.preventDefault();
      $("input[type=file]").trigger("click");
    });
    $("input[type=file]").change(function(){
      var file = $("input[type=file]")[0].files[0];            
      $("#preview").empty();
      displayAsImage3(file, "preview");
      
      $info = $("#info");
      $info.empty();
      if (file && file.name) {
        $info.append("<li>name:<span>" + file.name + "</span></li>");
      }
      if (file && file.type) {
        $info.append("<li>size:<span>" + file.type + " bytes</span></li>");
      }
      if (file && file.size) {
        $info.append("<li>size:<span>" + file.size + " bytes</span></li>");
      }
      if (file && file.lastModifiedDate) {
        $info.append("<li>lastModifiedDate:<span>" + file.lastModifiedDate + " bytes</span></li>");
      }
      $info.listview("refresh");
    });
    });
/*
function displayAsImage3(file, containerid) {
    if (typeof FileReader !== "undefined") {
      var container = document.getElementById(containerid),
          img = document.createElement("img"),
          reader;
      container.appendChild(img);
      reader = new FileReader();
      reader.onload = (function (theImg) {
        return function (evt) {
          theImg.src = evt.target.result;
        };
      }(img));
      reader.readAsDataURL(file);
    }
  }


  function previewFile(){
    var preview = document.querySelector('img'); //selects the query named img
    var file    = document.querySelector('input[type=file]').files[0]; //sames as here
    var reader  = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file); //reads the data as a URL
    } else {
        preview.src = "";
    }           
  };

  previewFile();  //calls the function named previewFile()

  function isUploadSupported() {
    if (navigator.userAgent.match(/(Android (1.0|1.1|1.5|1.6|2.0|2.1))|(Windows Phone (OS 7|8.0))|(XBLWP)|(ZuneWP)|(w(eb)?OSBrowser)|(webOS)|(Kindle\/(1.0|2.0|2.5|3.0))/)) {
        return false;
    }
    var elem = document.createElement('input');
    elem.type = 'file';
    return !elem.disabled;
  };

  function sendFile(fileData) {
  var formData = new FormData();

  formData.append('imageData', fileData);

  $.ajax({
    type: 'POST',
    url: '/your/upload/url',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      if (data.success) {
        alert('Your file was successfully uploaded!');
      } else {
        alert('There was an error uploading your file!');
      }
    },
    error: function (data) {
      alert('There was an error uploading your file!');
    }
  });
  }

  function readFile(file) {
  var reader = new FileReader();

  reader.onloadend = function () {
    processFile(reader.result, file.type);
  }

  reader.onerror = function () {
    alert('There was an error reading the file!');
  }

  reader.readAsDataURL(file);
  }
  */
