$(document).ready(function() {
    var search_results = document.getElementById("search-results");
    var searchUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    var shopUrl = "https://bookshop.org/search?keywords=";
    var apiKey = "";
    var placeHldr = '<img src="images/placeholder.jpg">';
    var search_data;

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
                        $("#title").animate({'marginTop': '-30px'}, 1000);
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
          bookIsbn = (item.volumeInfo.industryIdentifiers[1] && item.volumeInfo.industryIdentifiers[1].type === "ISBN_13") ? item.volumeInfo.industryIdentifiers[1].identifier : item.volumeInfo.industryIdentifiers[0].identifier ;
          bookImg1 = (item.volumeInfo.imageLinks) ? item.volumeInfo.imageLinks.thumbnail : placeHldr ;
  
          item2 = response.items[i+1];
          title2 = item2.volumeInfo.title;
          author2 = item2.volumeInfo.authors;
          description2 = item2.volumeInfo.description;
          bookLink2 = item2.volumeInfo.previewLink;
          bookIsbn2 = (item2.volumeInfo.industryIdentifiers[1] && item2.volumeInfo.industryIdentifiers[1].type === "ISBN_13") ? item2.volumeInfo.industryIdentifiers[1].identifier : item2.volumeInfo.industryIdentifiers[0].identifier ;
          bookImg2 = (item2.volumeInfo.imageLinks) ? item2.volumeInfo.imageLinks.thumbnail : placeHldr ;
  
          search_results.innerHTML += '<div class="row mt-4">' +
                                  formatOutput(bookImg1, title1, author1, description1, bookLink1, bookIsbn) +
                                  formatOutput(bookImg2, title2, author2, description2, bookLink2, bookIsbn2) +
                                  '</div>';
  
          console.log(search_results);
        }
     }

     function formatOutput(bookImg, title, author, description, bookLink, bookIsbn) {
        var buyUrl = shopUrl+bookIsbn; //link to bookstore
        var htmlCard = `<div class="col-lg-6">
          <div class="card" style="">
            <div class="row no-gutters">
              <div class="col-md-4">
                <img src="${bookImg}" class="card-img" alt="...">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">${title}</h5>
                  <p class="card-text">Author: ${author}</p>
                  <p class="card-text">${description}</p>
                  <p class="card-text">${bookIsbn}</p>
                    <p>
                        <a href="index.html" class="btn btn-primary">Add to Library</a>
                        <a target="_blank" href="${bookLink}" class="btn btn-primary">Preview</a>
                        <a target="_blank" href="${buyUrl}" class="btn btn-primary">Buy Book</a>
                    </p>
                </div>
              </div>
            </div>
          </div>
        </div>`
        return htmlCard;
      }

});


