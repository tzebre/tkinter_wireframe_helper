window.onload = function () {
    var canvasContainer = document.getElementById("white_board");
    var canvas = document.getElementById("canvas")
    var resize_btn = document.getElementById("refresh")
    var delete_btn = document.getElementById("delete_rect")
    var drop_btn = document.getElementById("myDropdown")
    var save_btn = document.getElementById("saveAllBtn")
    var height_btn = document.getElementById("height")
    var width_btn = document.getElementById("width")
    var x_btn = document.getElementById("x")
    var y_btn = document.getElementById("y")
    var context = canvas.getContext("2d");
    var isDrawing = false;
    var rect = {};
    var aspectRatio = 16 / 9
    var canvasRect = canvas.getBoundingClientRect();
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", drawRectangle);
    canvas.addEventListener("mouseup", stopDrawing);
    delete_btn.addEventListener("click", delete_widget)
    drop_btn.addEventListener("change", dropchange)
    save_btn.addEventListener("click", save_all)
    height_btn.addEventListener("input", size_change)
    width_btn.addEventListener("input", size_change)
    x_btn.addEventListener("input", size_change)
    y_btn.addEventListener("input", size_change)
    resize_btn.addEventListener("click", function () {
        resizeCanvas();
        window.location.href = '/';
    })
    resizeCanvas()

    function size_change() {
        modify_widget(x_btn.value, y_btn.value, height_btn.value, width_btn.value)
    }

    function modify_widget(x, y, h, w) {
        verify_border(parseInt(x), parseInt(x) + parseInt(w), parseInt(y), parseInt(y) + parseInt(h))
    }

    function verify_border(start, end, top, bottom) {
        console.log(start, end, top, bottom)
        console.log(canvas.width, canvas.height)
        if (bottom >= canvas.height) {
            if (top > 0) {
                y_btn.value = parseInt(y_btn.value) - 1
            } else {
                height_btn.value = parseInt(height_btn.value) - 1
            }

        } else {
            if (end >= canvas.width) {
                if (start > 0) {
                    x_btn.value = parseInt(x_btn.value) - 1
                } else {
                    width_btn.value = parseInt(width_btn.value) - 1
                }
            }
        }
    }

    function save_all() {
        window.location.href = '/save_all';
    }

    function dropchange() {
        console.log(drop_btn.value)
        drop_dict = {
            type: drop_btn.value
        }
        fetch('/drop_choice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(drop_dict)
        })
            .then(response => {
                // Handle the response from Flask
                window.location.href = '/';


            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function delete_widget() {
        let name = document.getElementById("selected_rect")
        let dict_del = {
            name: name.textContent
        }
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dict_del)
        })
            .then(response => {
                // Handle the response from Flask
                window.location.href = '/';


            })
            .catch(error => {
                console.error('Error:', error);
            });

    }


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
        /*
        let offsetX = (containerWidth - canvasWidth) / 2;
        let offsetY = (containerHeight - canvasHeight) / 2;

        canvas.style.left = offsetX + "px";
        canvas.style.top = offsetY + "px";

         */
        let offsetX = 0
        let offsetY = 0

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
        if (x < 0) {
            x = 0
        }
        if (y < 0) {
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
        openPopup()

        function openPopup() {
            let name = prompt("Please enter widget name:");
            if (name) {
                let element = document.getElementById(name);
                if (element) {
                    alert('Choice Incorrect: ID already exists');
                } else {

                    let res_dict = {
                            name: name,
                            coords: {
                                x: rect.startX / canvas.width * 100,
                                y: rect.startY / canvas.height * 100,
                                width: width / canvas.width * 100,
                                height: height / canvas.height * 100,
                            }
                        }
                    ;
                    fetch('/new_widget', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(res_dict)
                    })
                        .then(response => {
                            // Handle the response from Flask
                            window.location.href = '/';
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });


                }
            } else {
                context.clearRect(0, 0, canvas.width, canvas.height);
            }

        }
    }

    var clickableElements = document.querySelectorAll('.widget');

    clickableElements.forEach(function (element) {
        element.addEventListener('click', function () {
            // Code to execute when the element is clicked
            let selected_widget = {
                name: element.id,
            }

            fetch('/select_widget', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(selected_widget)
            })
                .then(response => {
                    // Handle the response from Flask
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        });
    });
}





