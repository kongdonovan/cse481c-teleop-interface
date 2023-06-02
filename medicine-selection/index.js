(function() {
    window.addEventListener("load", init)

    const id = element => {return document.getElementById(element);}

    // initializes all buttons to make fetch requests to our backend
    // once
    function init() {
        console.log("test")
        id("medicine-1").addEventListener("click", getMedicine1);
    }

    // makes a fetch request to the robot telling it to get medicine 1
    function getMedicine1() {
        console.log("dsafasdf");
        fetch('http://172.28.7.121:5000/get_medicine?type=origin')
    }

})()