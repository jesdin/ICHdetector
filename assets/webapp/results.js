var i = 0, text;
text = "RESULTS FROM INTRACRANIAL HEMORRHAGE MODEL:";
function typing() {
    if (i < text.length) {
        document.getElementById("results").innerHTML += text.charAt(i);
        i++;
        setTimeout(typing, 100);
    }
}
//Waiting for the function to load
$(document).ready(function () {
    // console.log({{ name }});
    typing();
    $('#image_name').delay(5000).show(0);
    $('#hemorrhage_image').delay(5000).show(0);
});