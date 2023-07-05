window.addEventListener('resize', resizeCanvas);

function resizeCanvas() {
    var parentDiv = document.getElementById('white_board');
    var childDiv = parentDiv.querySelector('#canvas');
    var Width = parentDiv.clientWidth;
    var Height = parentDiv.clientHeight;
    var aspectRatio = Width / Height;
    var limitingDimension = aspectRatio < 1.7778 ? 'width' : 'height';

    // Calculate the width and height of the maximum 16:9 rectangle based on the limiting dimension
    var max169Width = limitingDimension === 'width' ? Width : Height * 1.7778;
    var max169Height = limitingDimension === 'height' ? Height : Width / 1.7778;
    childDiv.style.height = max169Height + "px"
    childDiv.style.width = max169Width + "px"


}

resizeCanvas()

window.onload = function () {
    var canvas = document.getElementById('canvas')
    var ctx = canvas.getContext("2d");
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', drawRectangle);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);
    var isDrawing = false;
    var startPosition = {x: 0, y: 0};
    var currentRectangle = {x: 0, y: 0, width: 0, height: 0};

    function startDrawing(event) {
        isDrawing = true;
        startPosition.x = event.clientX - canvas.offsetLeft;
        startPosition.y = event.clientY - canvas.offsetTop;
    }

    function drawRectangle(event) {
        if (!isDrawing) return;

        var currentX = event.clientX - canvas.offsetLeft;
        var currentY = event.clientY - canvas.offsetTop;
        currentRectangle.x = Math.min(startPosition.x, currentX);
        currentRectangle.y = Math.min(startPosition.y, currentY);
        currentRectangle.width = Math.abs(currentX - startPosition.x);
        currentRectangle.height = Math.abs(currentY - startPosition.y);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeRect(
            currentRectangle.x,
            currentRectangle.y,
            currentRectangle.width,
            currentRectangle.height
        );
    }

    function stopDrawing() {
        isDrawing = false;
    }
}