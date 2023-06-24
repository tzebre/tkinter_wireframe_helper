window.onload = function () {
    var rectanglesContainer = document.getElementById("canvasContainer");
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");
    var aspectRatio = 16 / 9;

    function resizeCanvas() {
        var containerWidth = canvasContainer.offsetWidth;
        var containerHeight = canvasContainer.offsetHeight;

        if (containerWidth / containerHeight > aspectRatio) {
            var canvasWidth = containerHeight * aspectRatio;
            var canvasHeight = containerHeight;
        } else {
            var canvasWidth = containerWidth;
            var canvasHeight = containerWidth / aspectRatio;
        }

        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        var offsetX = (containerWidth - canvasWidth) / 2;
        var offsetY = (containerHeight - canvasHeight) / 2;

        canvas.style.left = offsetX + "px";
        canvas.style.top = offsetY + "px";
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    var isDrawing = false;
    var rect = {};

    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", drawRectangle);
    canvas.addEventListener("mouseup", stopDrawing);

    function startDrawing(event) {
        isDrawing = true;
        rect.startX = event.clientX - canvas.offsetLeft;
        rect.startY = event.clientY - canvas.offsetTop;
    }

    function drawRectangle(event) {
        if (!isDrawing) return;

        var x = event.clientX - canvas.offsetLeft;
        var y = event.clientY - canvas.offsetTop;

        var width = x - rect.startX;
        var height = y - rect.startY;

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.strokeRect(rect.startX, rect.startY, width, height);
    }

    function stopDrawing() {
        isDrawing = false;
        var width = event.clientX - canvas.offsetLeft - rect.startX;
        var height = event.clientY - canvas.offsetTop - rect.startY;

        openPopup(rect.startX, rect.startY, width, height);
    }

    function openPopup(startX, startY, width, height) {
        var name = prompt("Enter a name for the rectangle:");
        if (name) {
            var rectangle = {
                startX: startX,
                startY: startY,
                width: width,
                height: height,
                name: name
            };
            saveRectangle(rectangle);
        }
    }

    function saveRectangle(rectangle) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/save_rectangle");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    createRectangleDiv(rectangle);
                } else {
                    console.error(xhr.statusText);
                }
            }
        };
        xhr.send(JSON.stringify(rectangle));
    }
    function createRectangleDiv(rectangle) {
        var rectDiv = document.createElement("div");
        rectDiv.className = "rectangle";
        rectDiv.style.position = "absolute";
        rectDiv.style.left = rectangle.startX + "px";
        rectDiv.style.top = rectangle.startY + "px";
        rectDiv.style.width = rectangle.width + "px";
        rectDiv.style.height = rectangle.height + "px";
        rectDiv.style.backgroundColor = "red";
        rectanglesContainer.appendChild(rectDiv);
    }
};
