document.addEventListener("DOMContentLoaded", function() {
    var sector = document.getElementById('bg').getAttribute('data-sector');
    var bgElement = document.getElementById("bg");

    var baseUrl = "/static/img/";

    if (sector == 'it') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "it.png')";
    } else if (sector == 'finance') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "finance.png')";
    } else if (sector == 'media') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "media.png')";
    } else if (sector == 'education') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "education.png')";
    } else if (sector == 'manufacturing') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "manufacturing.png')";
    } else if (sector == 'agriculture') {
        bgElement.style.backgroundImage = "url('" + baseUrl + "agriculture.png')";
    }
});