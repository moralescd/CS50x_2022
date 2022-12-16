$(document).ready(function() {
    var search_results = document.getElementById("search-results");
    var searchUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    var printUrl = "https://bookshop.org/search?keywords=";
    var audioUrl = "https://libro.fm/search?utf8=%E2%9C%93&q=";
    var ebookUrl = "https://www.kobo.com/us/en/search?query=";
    var placeHldr = "static/favicon.ico";
    var search_data;

    // search on 'enter'
    var input = document.getElementById("search-box");
    input.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("search").click();
      }
    });

    // search listener
    $("#search").click(function() {
        search_results.innerHTML = "";
        search_data = $("#search-box").val();
        // empty search field
        if(search_data === "" || search_data === null) {
            alert("Error: No search term entered.");
        }
        else {
            $.ajax({
                url: searchUrl + search_data,
                dataType: "json",
                success: function(response) {
                    console.log(response)
                    if(response.totalItem === 0) {
                        alert("No results found...")
                    }
                    else {
                        $("#title").animate({'marginTop': '-10px'}, 1000);
                        $(".results").css("visibility", "visible");
                        displayResults(response);
                    }
                },
                error: function() {
                    alert("Something went wrong... Try again.");
                }
            });
        }
        $("#search-box").val("");
    });

    function displayResults(response) {
        for (var i = 0; i < response.items.length; i+=2) {
          item = response.items[i];
          title1 = item.volumeInfo.title;
          author1 = item.volumeInfo.authors;
          description1 = item.volumeInfo.description;
          bookLink1 = item.volumeInfo.previewLink;
          //bookIsbn = (item.volumeInfo.industryIdentifiers[1] && item.volumeInfo.industryIdentifiers[1].type === "ISBN_13") ? item.volumeInfo.industryIdentifiers[1].identifier : item.volumeInfo.industryIdentifiers[0].identifier ;
          bookImg1 = (item.volumeInfo.imageLinks) ? item.volumeInfo.imageLinks.thumbnail : placeHldr ;
          pageCount1 = item.volumeInfo.pageCount;

          item2 = response.items[i+1];
          title2 = item2.volumeInfo.title;
          author2 = item2.volumeInfo.authors;
          description2 = item2.volumeInfo.description;
          bookLink2 = item2.volumeInfo.previewLink;
          //bookIsbn2 = (item2.volumeInfo.industryIdentifiers[1] && item2.volumeInfo.industryIdentifiers[1].type === "ISBN_13") ? item2.volumeInfo.industryIdentifiers[1].identifier : item2.volumeInfo.industryIdentifiers[0].identifier ;
          bookImg2 = (item2.volumeInfo.imageLinks) ? item2.volumeInfo.imageLinks.thumbnail : placeHldr ;
          pageCount2 = item.volumeInfo.pageCount;

          search_results.innerHTML += '<div class="row mt-4">' +
                                  formatOutput(bookImg1, title1, author1, description1, bookLink1, pageCount1) +
                                  formatOutput(bookImg2, title2, author2, description2, bookLink2, pageCount2) +
                                  '</div>';

          console.log(search_results);
        }
     }

     function formatOutput(bookImg, title, author, description, bookLink, pageCount) {
        var buyprintUrl = printUrl+title+" "+author; //link to bookshop.org
        var buyebookUrl = ebookUrl+title+" "+author; //link to kobo
        var buyaudioUrl = audioUrl+title+" "+author; //link to libroFM
        var htmlCard = `<div class="col-lg-6">
          <div class="card" style="">
            <div class="row no-gutters">
              <div class="col-md-4">
                <img src=${bookImg} class="card-img" alt="...">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h4 class="card-title">${title}</h4>
                  <p class="card-text">Author: ${author}</p>
                  <p class="card-text">Page Count: ${pageCount}</p>
                  <div class="card-text text-block">${description}</div>
                  <br>
                  <div class="card-buttons">
                    <form action="/search" method="post">
                      <input type="hidden" id="title" name="title" value="${title}">
                      <input type="hidden" id="author" name="author" value="${author}">
                      <input type="hidden" id="pageCount" name="pageCount" value="${pageCount}">
                      <button class="btn btn-primary" type="submit">Add to Library</button>
                    </form>
                    <br>
                      <a target="_blank" href="${bookLink}" class="btn btn-primary">Preview</a>
                    <br><h5>Buy:</h5>
                      <a target="_blank" href="${buyprintUrl}" class="btn btn-primary">Print Book</a>
                      <a target="_blank" href="${buyebookUrl}" class="btn btn-primary">Ebook</a>
                      <a target="_blank" href="${buyaudioUrl}" class="btn btn-primary">Audiobook</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>`
        return htmlCard;
      }

});


