window.onload = function () {
    var canvasContainer = document.getElementById("white_board");
    var canvas = document.getElementById("canvas")
    var context = canvas.getContext("2d");
    var isDrawing = false;
    var rect = {};
    var aspectRatio = 16 / 9
    var canvasRect = canvas.getBoundingClientRect();
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", drawRectangle);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);
    resizeCanvas()


    function resizeCanvas() {
        let containerWidth = canvasContainer.offsetWidth;
        let containerHeight = canvasContainer.offsetHeight;
        let canvasWidth = 0;
        let canvasHeight = 0;

        if (containerWidth / containerHeight <= aspectRatio) {
            canvasWidth = containerWidth;
            canvasHeight = containerWidth / aspectRatio;
        } else {
            canvasWidth = containerHeight * aspectRatio;
            canvasHeight = containerHeight;
        }
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        let offsetX = (containerWidth - canvasWidth) / 2;
        let offsetY = (containerHeight - canvasHeight) / 2;

        canvas.style.left = offsetX + "px";
        canvas.style.top = offsetY + "px";
    }


window.addEventListener('resize', resizeCanvas);


function startDrawing(event) {
    isDrawing = true;
    rect.startX = event.clientX - canvasRect.left;
    rect.startY = event.clientY - canvasRect.top;
}

function drawRectangle(event) {
    if (!isDrawing) return;

    var x = event.clientX - canvasRect.left;
    var y = event.clientY - canvasRect.top;

    var width = x - rect.startX;
    var height = y - rect.startY;

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.strokeRect(rect.startX, rect.startY, width, height);
}

function stopDrawing() {
    isDrawing = false;
    var width = event.clientX - rect.startX - canvasContainer.left;
    var height = event.clientY - rect.startY - canvasContainer.top;
    if (width < 0) {
        width = -width
        rect.startX = rect.startX - width
    }
    if (height < 0) {
        height = -height
        rect.startY = rect.startY - height
    }
}


}



