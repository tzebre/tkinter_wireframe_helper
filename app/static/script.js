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
        console.log(rect.startX, rect.startY, width, height)
        if (width < 0) {
            width = -width
            rect.startX = rect.startX - width
        }
        if (height < 0) {
            height = -height
            rect.startY = rect.startY - height
        }
        console.log(rect.startX, rect.startY, width, height);


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
            context.clearRect(0, 0, canvas.width, canvas.height);
            createRectangleDiv(rectangle);
        }
    }


    function createRectangleDiv(rectangle) {
        var rectDiv = document.createElement("div");
        rectDiv.className = rectangle.name;
        rectDiv.id = "rectangle"
        rectDiv.style.position = "absolute";
        rectDiv.style.left = (rectangle.startX + canvas.offsetLeft) + "px";
        rectDiv.style.top = (rectangle.startY + canvas.offsetTop) + "px";
        rectDiv.style.width = rectangle.width + "px";
        rectDiv.style.height = rectangle.height + "px";
        rectDiv.style.backgroundColor = "red";

        var nameDiv = document.createElement("div");
        nameDiv.className = "rectangle-name";
        nameDiv.style.textAlign = "center";
        nameDiv.style.lineHeight = rectangle.height + "px";
        nameDiv.innerText = rectangle.name;
        var widthInput = document.createElement("input");
        widthInput.type = "number";
        widthInput.placeholder = "Width";
        widthInput.value = rectangle.width;

        var heightInput = document.createElement("input");
        heightInput.type = "number";
        heightInput.placeholder = "Height";
        heightInput.value = rectangle.height;
        var validateBtn = document.createElement("button");
        validateBtn.textContent = "Validate";
        validateBtn.addEventListener("click", function () {
            var width = parseInt(widthInput.value);
            var height = parseInt(heightInput.value);
            if (width > canvas.clientWidth) {
                width = canvas.clientWidth;
            }
            if (height > canvas.clientHeight) {
                height = canvas.clientHeight;
            }

            if (!isNaN(width) && !isNaN(height) && width > 0 && height > 0) {
                rectangle.width = width;
                rectangle.height = height;
                rectDiv.style.width = width + "px";
                rectDiv.style.height = height + "px";
            }

            widthInput.value = rectangle.width;
            heightInput.value = rectangle.height;
            console.log("before", rectDiv.offsetTop, rectDiv.offsetLeft)
            verify_placement(rectDiv.offsetLeft, rectDiv.offsetTop)

        });


        var dropdownBtn = document.createElement("button");
        dropdownBtn.className = "dropdown-button";
        dropdownBtn.textContent = "Options";
        rectDiv.appendChild(widthInput);
        rectDiv.appendChild(heightInput);
        rectDiv.appendChild(dropdownBtn);
        rectDiv.appendChild(validateBtn)
        rectDiv.appendChild(nameDiv);

        rectanglesContainer.appendChild(rectDiv);
        rectDiv.addEventListener("mousedown", startDrag);


        var offsetX, offsetY;
        var isDragging = false;

        function startDrag(event) {
            isDragging = true
            offsetX = event.clientX - rectDiv.offsetLeft;
            offsetY = event.clientY - rectDiv.offsetTop;
            console.log("start", offsetX, offsetY, event.clientX, event.clientY)
            rectDiv.addEventListener("mousemove", handleDrag);
            rectDiv.addEventListener("mouseup", stopDrag);

        }

        function verify_placement(x, y) {
            var minX = canvas.offsetLeft;
            var minY = canvas.offsetTop;
            var maxX = canvas.offsetLeft + canvas.offsetWidth - rectDiv.offsetWidth;
            var maxY = canvas.offsetTop + canvas.offsetHeight - rectDiv.offsetHeight;

            // Check if the new coordinates exceed the canvas boundaries
            if (x > maxX) {
                x = maxX;
            } else if (x < minX) {
                x = minX
            }

            if (y > maxY) {
                y = maxY;
            } else if (y < minY) {
                y = minY;
            }
            console.log(x, y)
            rectDiv.style.left = x + "px";
            rectDiv.style.top = y + "px";
        }

        function handleDrag(event) {
            if (isDragging) {
                var x = event.clientX - offsetX;
                var y = event.clientY - offsetY;
                verify_placement(x, y)
            }
        }


        function saveRectanglePosition(name, left, top) {

            rectDiv.style.left = left
            rectDiv.style.top = top
        }


        function stopDrag() {
            isDragging = false;
            rectDiv.addEventListener("mousemove", handleDrag);
            rectDiv.addEventListener("mouseup", stopDrag);
            // Update the position values in the rectangle object
            rectDiv.style.left = (parseFloat(rectDiv.style.left)) + "px";
            rectDiv.style.top = (parseFloat(rectDiv.style.top)) + "px";


            // Save the updated rectangle position if needed
            saveRectanglePosition(rectDiv.name, rectDiv.style.left, rectDiv.style.top);

        }
    }

    var saveAllBtn = document.getElementById("saveAllBtn");
    saveAllBtn.addEventListener("click", saveAllRectangles);

    function saveAllRectangles() {
        var rectangles = {};
        var rectangleDivs = document.querySelectorAll('[id="rectangle"]');
        console.info(rectangleDivs)

        for (var i = 0; i < rectangleDivs.length; i++) {
            var rectDiv = rectangleDivs[i];
            var name = rectDiv.className;
            var rectangle = {
                startX: parseInt(rectDiv.style.left) - canvas.offsetLeft,
                startY: parseInt(rectDiv.style.top) - canvas.offsetTop,
                width: parseInt(rectDiv.style.width),
                height: parseInt(rectDiv.style.height)
            };

            rectangles[name] = rectangle;
        }
        rectangles["canvas_size"] = {"width": canvas.clientWidth, "height": canvas.clientHeight}

        var jsonData = JSON.stringify([rectangles]);
        console.log(jsonData);

        fetch('/save_all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({rectangles: rectangles}),
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response or perform any necessary actions
                console.log('Save all response:', data);
            })
            .catch(error => {
                // Handle any errors that occurred during the request
                console.error('Error saving all rectangles:', error);
            });
    }


}
;
