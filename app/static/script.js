window.addEventListener('resize', resizeCanvas);

function resizeCanvas() {
    var parentDiv = document.getElementById('white_board');
    var childDiv = parentDiv.querySelector('#canvas');
    var Width = parentDiv.clientWidth;
    var Height = parentDiv.clientHeight;
    console.log("W", Width, "H", Height)
    var aspectRatio = Width / Height;
    var limitingDimension = aspectRatio < 1.7778 ? 'width' : 'height';
    console.log(aspectRatio, limitingDimension)

    // Calculate the width and height of the maximum 16:9 rectangle based on the limiting dimension
    var max169Width = limitingDimension === 'width' ? Width : Height * 1.7778;
    var max169Height = limitingDimension === 'height' ? Height : Width / 1.7778;
    console.log("mH", max169Height, "mW", max169Width)
    childDiv.style.height = max169Height + "px"
    childDiv.style.width = max169Width + "px"


}

resizeCanvas()