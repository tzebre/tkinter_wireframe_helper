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

        let res_dict = {
            x: offsetX,
            y: offsetY,
            width: canvasWidth,
            height: canvasHeight,
        };
        fetch('/resize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(res_dict)
        })
            .then(response => {
                // Handle the response from Flask
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    window.addEventListener('resize', resizeCanvas);


    function startDrawing(event) {
        isDrawing = true;
        rect.startX = event.clientX - canvasRect.left;
        rect.startY = event.clientY - canvasRect.top;
    }

    function drawRectangle(event) {
        if (!isDrawing) return;

        let x = event.clientX - canvasRect.left;
        let y = event.clientY - canvasRect.top;

        let width = x - rect.startX;
        let height = y - rect.startY;

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.strokeRect(rect.startX, rect.startY, width, height);
    }

    function stopDrawing(event) {
        isDrawing = false;
        let x = event.clientX - canvasRect.left;
        let y = event.clientY - canvasRect.top;
        if (x < 0){
            x = 0
        }
        if (y <0){
            y = 0
        }
        let width = x - rect.startX;
        let height = y - rect.startY;
        if (width < 0) {
            width = -width
            rect.startX = rect.startX - width
        }
        if (height < 0) {
            height = -height
            rect.startY = rect.startY - height
        }
        console.log(rect.startX, rect.startY, height, width, canvas.width, canvas.height)

        let res_dict = {
            x: rect.startX / canvas.width * 100,
            y: rect.startY / canvas.height * 100,
            width: width / canvas.width * 100,
            height: height / canvas.height * 100,
        };
        fetch('/new_widget', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(res_dict)
        })
            .then(response => {
                // Handle the response from Flask
            })
            .catch(error => {
                console.error('Error:', error);
            });

    }
}



