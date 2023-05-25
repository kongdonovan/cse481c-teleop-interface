(function() {
    window.addEventListener("load", init)

    function init() {
        document.getElementById("armup").addEventListener("click", moveup)
        document.getElementById("armdown").addEventListener("click", movedown)
        document.getElementById("extend").addEventListener("click", extend)
        document.getElementById("grip").addEventListener("click", grip)
        document.getElementById("release").addEventListener("click", release)
        document.getElementById("retract").addEventListener("click", retract)
        document.getElementById("forward").addEventListener("click", forward)
        document.getElementById("back").addEventListener("click", backward)
        document.getElementById("left").addEventListener("click", left)
        document.getElementById("right").addEventListener("click", right)
    }

    function extend() {
        fetch("http://172.28.7.121:5000/extend_arm")
        .catch(console.log)
    }

    function grip() {
        fetch("http://172.28.7.121:5000/grip")
        .catch(console.log)
    }

    function release() {
        fetch("http://172.28.7.121:5000/release_grip")
        .catch(console.log)
    }

    function retract() {
        fetch("http://172.28.7.121:5000/retract_arm")
        .catch(console.log)
    }

    function moveup() {
        fetch("http://172.28.7.121:5000/move_arm_up")
        .catch(console.log)
    }

    function movedown() {
        fetch("http://172.28.7.121:5000/move_arm_down")
        .catch(console.log)
    }

    function forward() {
        fetch("http://172.28.7.121:5000/move_forward")
        .catch(console.log)
    }

    function backward() {
        fetch("http://172.28.7.121:5000/move_backwards")
        .catch(console.log)
    }

    function left() {
        fetch("http://172.28.7.121:5000/turn_left")
        .catch(console.log)
    }

    function right() {
        fetch("http://172.28.7.121:5000/turn_right")
        .catch(console.log)
    }
})()