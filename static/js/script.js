const pages = ["Encode", "Decode"];

$(document).ready(function () {
  setupFunctions();
  renderNavPage();
  setPage(pages[0]);
  setTitle(pages[0]);
  renderOutputText();
  checkIsSubmitted();
});

function checkIsSubmitted() {
  if (localStorage.getItem("submitted") === "true") {
    localStorage.removeItem("submitted");
    afterSubmit();
  } else {
    beforeSubmit();
  }
}

function beforeSubmit() {
  $("#image-source").hide();
  $("#image-size").hide();
}

function renderOutputText() {
  if (encodedText) {
    let totalRowsText = (encodedText.match(/\n/g) || []).length + 1;
    let totalRowsCodebook = Object.keys(codebook).length;
    let totalRows = totalRowsText + totalRowsCodebook + 3;

    $("#encoded_text").attr("rows", totalRows);

    let formattedText = "Encoded Text:\n" + encodedText + "\n\nCodebook:\n";
    $.each(codebook, function (char, code) {
      formattedText += char + ": " + code + "\n";
    });
    $("#encoded_text").val(formattedText);
  }
}

function setupFunctions() {
  $("#inputImage").on("change", previewImage);
  $("#form-image").on("submit", () => {
    localStorage.setItem("submitted", "true");
    localStorage.setItem("whichForm", "image");
    $("#image-source").show();
    $("#image-size").show();
  });
  $("#form-text").on("submit", () => {
    localStorage.setItem("submitted", "true");
    localStorage.setItem("whichForm", "text");
    localStorage.setItem("textData", JSON.stringify($("#text-input").val()));
  });

  if (localStorage.getItem("imageData") === null) {
    localStorage.setItem("imageData", JSON.stringify({ source: "", size: "" }));
  }

  let navIsOpen = false;
  $("#btn-navbar")
    .off("click")
    .on("click", function () {
      if (navIsOpen === false) {
        $("#icon-navbar").removeClass("fa-bars").addClass("fa-xmark");
        $("#navbar-default").slideDown(200);
      } else {
        $("#icon-navbar").removeClass("fa-xmark").addClass("fa-bars");
        $("#navbar-default").slideUp(200);
      }

      navIsOpen = !navIsOpen;
    });
}

function afterSubmit() {
  let imageData = JSON.parse(localStorage.getItem("imageData"));
  let textData = JSON.parse(localStorage.getItem("textData"));
  let whichForm = localStorage.getItem("whichForm");

  if (whichForm === "text") {
    setPage(pages[0]);
    setNavPage(pages[0]);
    setTitle(pages[0]);
    $("#text-input").val(textData);
  } else {
    setPage(pages[1]);
    setNavPage(pages[1]);
    setTitle(pages[1]);
    $("#placeholder-image-source").hide();
    $("#placeholder-image-size").hide();
    $("#imagePreview").attr("src", imageData.source);
    $("#fileSize").text(imageData.size + " mb");
  }
}

function previewImage(event) {
  let file = event.target.files[0];
  if (file) {
    let reader = new FileReader();
    reader.onload = function () {
      let imageSource = reader.result;
      $("#imagePreview").attr("src", imageSource);
      setFormData("source", imageSource);
    };
    reader.readAsDataURL(file);

    let fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    $("#fileSize").text("File size: " + fileSizeMB + " MB");
    setFormData("size", fileSizeMB);
  }
}

function setFormData(key, value) {
  console.log(value);
  let imageData = JSON.parse(localStorage.getItem("imageData"));
  switch (key) {
    case "source":
      imageData.source = value;
      break;
    case "size":
      imageData.size = value;
      break;
  }

  localStorage.setItem("imageData", JSON.stringify(imageData));
}

function renderNavPage() {
  for (let i = 0; i < pages.length; i++) {
    let liElement = $("<li>")
      .attr("data-page", pages[i])
      .addClass("group relative w-full rounded border-2 border-green-600 px-1 py-0.5 text-center md:border-none md:border-0 md:p-0 nav-page ")
      .on("click", function () {
        setPage(pages[i]);
        setNavPage(pages[i]);
        setTitle(pages[i]);
      });

    let aElement = $("<a>").attr("href", "#").addClass("text-xs md:text-sm lg:text-base font-bold capitalized").text(pages[i]);

    let divElement = $("<div>").addClass("absolute -bottom-1 h-1 bg-green-600 duration-300 md:group-hover:w-full hidden md:block");

    if (pages[i] === pages[0]) {
      liElement.addClass("bg-green-600 md:bg-white text-white md:text-black");
      divElement.addClass("w-full");
    } else {
      divElement.addClass("w-0");
    }

    liElement.append(aElement).append(divElement);
    $("#nav-menu").append(liElement);
  }
}

function setPage(page) {
  $(".page").each(function () {
    $(this).fadeOut(0);
    if ($(this).attr("id") === page.toLowerCase()) {
      $(this).fadeIn(100);
    }
  });
}

function setTitle(page) {
  let explainer;

  switch (page) {
    case "Text":
      explainer = "encode";
      break;
    case "Image":
      explainer = "compression";
      break;
    case "About":
      explainer = "this project";
      break;
  }
  $("title").text(`${page}`);
}

function setNavPage(page) {
  if ($(window).innerWidth() <= 768) {
    $(".nav-page").each(function () {
      $(this).removeClass("bg-green-600 text-white").addClass("bg-white text-black");
      if ($(this).data("page") === page) {
        $(this).addClass("bg-green-600 text-white").removeClass("bg-white text-black");
      }
    });
  } else {
    $(".nav-page").each(function () {
      $(this).find("div").removeClass("w-full").addClass("w-0");
      if ($(this).data("page") === page) {
        $(this).find("div").removeClass("w-0").addClass("w-full");
      }
    });
  }
}
