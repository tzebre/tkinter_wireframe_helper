window.onload = function () {
    var canvasContainer = document.getElementById("canvasContainer");
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");
    var aspectRatio = 16 / 9;
    var isDrawing = false;
    var rect = {};

    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", drawRectangle);
    canvas.addEventListener("mouseup", stopDrawing);

    function resizeCanvas() {
        console.log("resizing")
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

    // Rectangles draw
    function startDrawing(event) {
        isDrawing = true;
        rect.startX = event.clientX - canvasContainer.offsetLeft;
        rect.startY = event.clientY - canvasContainer.offsetTop;
    }

    function drawRectangle(event) {
        if (!isDrawing) return;

        var x = event.clientX - canvasContainer.offsetLeft;
        var y = event.clientY - canvasContainer.offsetTop;

        var width = x - rect.startX;
        var height = y - rect.startY;

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.strokeRect(rect.startX, rect.startY, width, height);
    }

    function stopDrawing() {
        isDrawing = false;
        var width = event.clientX - rect.startX - canvasContainer.offsetLeft;
        var height = event.clientY - rect.startY - canvasContainer.offsetTop;
        if (width < 0) {
            width = -width
            rect.startX = rect.startX - width
        }
        if (height < 0) {
            height = -height
            rect.startY = rect.startY - height
        }
        openPopup(rect.startX, rect.startY, width, height);
    }

    // Save rectangle into div
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
        rectDiv.style.left = ((rectangle.startX + canvas.offsetLeft) / canvas.clientWidth * 100) + "%";
        rectDiv.style.top = ((rectangle.startY + canvas.offsetTop) / canvas.clientHeight * 100) + "%";
        rectDiv.style.width = ((rectangle.width / canvas.clientWidth) * 100) + "%";
        rectDiv.style.height = ((rectangle.height / canvas.clientHeight) * 100) + "%";
        rectDiv.style.backgroundColor = "red";

        var nameDiv = document.createElement("div");
        nameDiv.className = "rectangle-name";
        nameDiv.innerText = rectangle.name;
        var widthInput = document.createElement("input");
        widthInput.type = "number";
        widthInput.placeholder = "Width";
        widthInput.value = rectangle.width;
        widthInput.style.width = 3 + "rem"
        widthInput.addEventListener("input", update_size);


        var heightInput = document.createElement("input");
        heightInput.type = "number";
        heightInput.placeholder = "Height";
        heightInput.value = rectangle.height;
        heightInput.style.width = 3 + "rem"
        heightInput.addEventListener("input", update_size);


        var dropdownBtn = document.createElement("button");
        dropdownBtn.className = "dropdown-button";
        fetch('/get_dropdown_values')
            .then(response => response.json())
            .then(data => {
                // Process the received data
                populateDropdown(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });

        function populateDropdown(values) {
            var dropdown = document.createElement('select');
            dropdown.className = 'dropdown';

            values.forEach(value => {
                var option = document.createElement('option');
                option.textContent = value;
                dropdown.appendChild(option);
            });

            dropdownBtn.appendChild(dropdown);
        }

        function deleteRectangle(rectDiv) {
            if (confirm("Are you sure you want to delete this rectangle?")) {
                rectDiv.parentNode.removeChild(rectDiv);
            }
        }

        var deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.addEventListener("click", function () {
            deleteRectangle(rectDiv);
        });
        var hideBtn = document.createElement("button");
        hideBtn.textContent = "Hide";
        hideBtn.addEventListener("click", function () {
            hideChildren(rectDiv, hideBtn);
        });

        function hideChildren(rectDiv, hideBtn) {
            var children = rectDiv.children;
            for (var i = 0; i < children.length; i++) {
                var child = children[i];
                if (child !== hideBtn) {
                    if (child.style.display === "none") {
                        child.style.display = "";
                        hideBtn.textContent = "Hide";
                    } else {
                        child.style.display = "none";
                        hideBtn.textContent = "Show";
                    }
                }
            }
        }


        rectDiv.appendChild(hideBtn);
        rectDiv.appendChild(widthInput);
        rectDiv.appendChild(heightInput);
        rectDiv.appendChild(dropdownBtn);
        rectDiv.appendChild(deleteBtn);
        rectDiv.appendChild(nameDiv);


        // Update div rectangle size
        function update_size() {
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
                rectDiv.style.width = ((width / canvas.clientWidth) * 100) + "%";
                rectDiv.style.height = ((height / canvas.clientHeight) * 100) + "%";
            }

            widthInput.value = rectangle.width;
            heightInput.value = rectangle.height;
            verify_placement(rectDiv.offsetLeft, rectDiv.offsetTop)

        }

        canvasContainer.appendChild(rectDiv);

        // Move div rectangle
        rectDiv.addEventListener("mousedown", startDrag);
        var offsetX, offsetY;
        var isDragging = false;

        function startDrag(event) {
            isDragging = true
            offsetX = event.clientX - rectDiv.offsetLeft;
            offsetY = event.clientY - rectDiv.offsetTop;
            rectDiv.addEventListener("mousemove", handleDrag);
            rectDiv.addEventListener("mouseup", stopDrag);
        }

        function handleDrag(event) {
            if (isDragging) {
                var x = event.clientX - offsetX;
                var y = event.clientY - offsetY;
                verify_placement(x, y)
            }
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

            rectDiv.style.left = ((x / canvas.clientWidth) * 100) + "%";
            rectDiv.style.top = ((y / canvas.clientHeight) * 100) + "%";
        }


        function stopDrag() {
            isDragging = false;
            rectDiv.addEventListener("mousemove", handleDrag);
            rectDiv.addEventListener("mouseup", stopDrag);

            saveRectanglePosition(rectDiv.name, rectDiv.style.left, rectDiv.style.top);

        }

        function saveRectanglePosition(name, left, top) {
            rectDiv.style.left = left
            rectDiv.style.top = top
        }

        // Save results
        var saveAllBtn = document.getElementById("saveAllBtn");
        saveAllBtn.addEventListener("click", saveAllRectangles);

        function saveAllRectangles() {
            var rectangles = {};
            var rectangleDivs = document.querySelectorAll('[id="rectangle"]');

            for (var i = 0; i < rectangleDivs.length; i++) {
                var rectDiv = rectangleDivs[i];
                var name = rectDiv.className;
                var dropdown = rectDiv.querySelector('.dropdown');
                rectangles[name] = {
                    startX: parseFloat(rectDiv.style.left),
                    startY: parseFloat(rectDiv.style.top),
                    width: parseFloat(rectDiv.style.width),
                    height: parseFloat(rectDiv.style.height),
                    dropdownValue: dropdown.value
                };
            }
            var jsonData = JSON.stringify({rectangles: rectangles});

            fetch('/save_all', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: jsonData
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
}
