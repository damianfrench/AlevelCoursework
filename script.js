"use strict";

// async function change(){
//   console.log("waiting...")
//   await clicked();
//   console.log("received!!")

// }

// function clicked(){
//     document.addEventListener('keydown', function onKeyHander(e){
//       document.getElementById("R").innerHTML=e.key();
//       document.removeEventListener('keydown', arguments.callee);
//       resolve();
//       })
//     }

  const downloadFile = () => {
    const link = document.createElement("a");
    const content = document.getElementById("DocumentData").textContent;
    console.log(content)
    const file = new Blob([content], { type: 'text/plain' });
    link.href = URL.createObjectURL(file);
    link.download = "sample.txt";
    link.click();
    URL.revokeObjectURL(link.href);
  
}

const Info=["this program will record, analyse and output your speech when you press the record button","in the settings menu you will find a slider to tell the program how noisy your environment is, 3 sliders to control the colour scheme and then 2 buttons to control the keybinds that let you record and stop without pressing the buttons. Enjoy!!"];
var Pagenum=0;
window.onload=function(){
  document.getElementById('Info').innerHTML="welcome to Damian's Speech recognition program";
  document.getElementById('PageNumber').innerHTML="Step "+(Pagenum+1)
}

function nextInfo(){
  if(document.getElementById("nextPage").innerHTML=="Continue"){
    document.getElementById("buttonReference").setAttribute("href","Home");
    return
  }
  document.getElementById("Info").innerHTML=Info[Pagenum];
  Pagenum+=1;
  document.getElementById("PageNumber").innerHTML="Step "+(Pagenum+1);
  if(Pagenum==Info.length){
    document.getElementById("nextPage").innerHTML="Continue";
    return
  }
}

function RecordRequestDoc() {
  document.getElementById("RecordingInfo").innerHTML="Recording"
  fetch('/pythonRecord')
    .then(response => response.json())
    .then(data => {
      let output=""
      for(let i=0;i<data.length;i++){
        output+=data[i][0]
      }
      console.log(output)
      document.getElementById("DocumentData").insertAdjacentHTML("beforeend"," "+output)
      document.getElementById("RecordingInfo").innerHTML=""
      entering()
    });
}

document.addEventListener("keydown",function(event){
  if (event.key === "Enter"){
    fetch('/pythonRecord')
    .then(response => response.json())
    .then(data => {
      let output=""
      for(let i=0;i<data.length;i++){
        output+=data[i][0]
      }
      console.log(output)
      document.getElementById("DocumentData").insertAdjacentHTML("beforeend"," "+output)
      document.getElementById("RecordingInfo").innerHTML=""
  });
}
})

function StopRequestDoc() {
  document.getElementById("RecordingInfo").innerHTML="Stopping"
  fetch('/pythonStop')
    .then(response => response.json())
    .then(data => {
      if(data=="NA"){
        document.getElementById("RecordingInfo").innerHTML=""
        return;
      }
      let output=""
      for(let i=0;i<data.length;i++){
        output+=data[i][0]
      }
      document.getElementById("DocumentData").insertAdjacentHTML("beforeend"," "+output)
      document.getElementById("RecordingInfo").innerHTML=""
    });
}

function openPopup() {
  var html = "<h1>Hello World</h1>";
  var popup = window.open("", "PopupWindow", "width=500,height=500");
  popup.document.write(html);
}

// function changeRedColour(){
//   let currentColor = window.getComputedStyle(document.body).getPropertyValue("background-color");
//   console.log(currentColor)
//   let red = currentColor.substring(5, currentColor.indexOf(","));
//   console.log(red)
//   const slider = document.getElementById("red-slider");
//   const redValue = slider.value;
//   document.body.style.backgroundColor = "rgb(" + redValue + ", " + currentColor.substring(currentColor.indexOf(",") + 1);
//   }

// function changeBlueColour(){
//   let currentColor = window.getComputedStyle(document.body).getPropertyValue("background-color");
//   console.log(currentColor)
//   let blue = currentColor.substring(1, currentColor.indexOf(","));
//   console.log(blue)
//   const slider = document.getElementById("blue-slider");
//   const blueValue = slider.value;
//   document.body.style.backgroundColor = "rgb(" + BlueValue + ", " + currentColor.substring(currentColor.indexOf(",") + 1);
//   }

// function changeGreenColour(){
//   const slider = document.getElementById("green-slider");
//   const redValue = slider.value;
//     document.body.style.backgroundColor = `rgb(0, ${redValue}, 0)`;
//   }

const redSlider = document.querySelector("#red-slider");
const greenSlider = document.querySelector("#green-slider");
const blueSlider = document.querySelector("#blue-slider");
console.log(":)")
console.log(redSlider)

if(redSlider){
redSlider.addEventListener("input", () => {
  document.body.style.backgroundColor = `rgb(${redSlider.value}, ${greenSlider.value}, ${blueSlider.value})`;
  let color = document.body.style.backgroundColor
  fetch('/submitColour',{
    method : "POST",
    headers:{
      "Content-Type": "application/json"
    },
    body: JSON.stringify(color)
  })
  .then(response => response.text())
  .then(text => {
    console.log(text);
});
});
}
if(greenSlider){

greenSlider.addEventListener("input", () => {
  document.body.style.backgroundColor = `rgb(${redSlider.value}, ${greenSlider.value}, ${blueSlider.value})`;
  let color = document.body.style.backgroundColor
  fetch('/submitColour',{
    method : "POST",
    headers:{
      "Content-Type": "application/json"
    },
    body: JSON.stringify(color)
  })
  .then(response => response.text())
  .then(text => {
    console.log(text);
});
});
}
if(blueSlider){
blueSlider.addEventListener("input", () => {
  document.body.style.backgroundColor = `rgb(${redSlider.value}, ${greenSlider.value}, ${blueSlider.value})`;
  let color = document.body.style.backgroundColor
  fetch('/submitColour',{
    method : "POST",
    headers:{
      "Content-Type": "application/json"
    },
    body: JSON.stringify(color)
  })
  .then(response => response.text())
  .then(text => {
    console.log(text);
});
});
}
const button = document.getElementById("R");
var buttonValue="R"
if(button){
button.addEventListener("click", function() {
  document.addEventListener("keydown", function(event) {
    fetch('/RecordingButton',{
      method : "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify(event.key)
    })
    .then(response => response.text())
    .then(text => {
      console.log(text);
      location.reload();
  });
  },{ once: true });
});
localStorage.setItem('buttonValue',button.innerHTML)
}
var buttonValue=localStorage.getItem('buttonValue');
console.log("hellp")
console.log(localStorage.getItem('buttonValue'));

const buttonStop = document.getElementById("S");
console.log("button=",buttonStop)
var StopbuttonValue="S"
if(buttonStop){
buttonStop.addEventListener("click", function() {
  document.addEventListener("keydown", function(event) {
    fetch('/StoppingButton',{
      method : "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify(event.key)
    })
    .then(response => response.text())
    .then(text => {
      console.log(text);
      location.reload();
  });
  },{ once: true });
});
localStorage.setItem('StopbuttonValue',buttonStop.innerHTML)
}
var StopbuttonValue=localStorage.getItem('StopbuttonValue');
console.log("hellp")
console.log(localStorage.getItem('StopbuttonValue'));

// const button2 = document.getElementById("S");
// if(button2){
// button2.addEventListener("click", function() {
//   document.addEventListener("keydown", function(event) {
//     button2.innerText = event.key;
//   },{ once: true });
// });
// }

function updateBackgroundColor(color) {
  console.log(color)
  document.body.style.backgroundColor = color;
}
if(document.querySelector("#myVolumeRange")){
document.querySelector("#myVolumeRange").addEventListener("input", ()=> {
  let sound=document.getElementById("myVolumeRange").value;
  console.log(sound)
  fetch('/submitSound',{
    method : "POST",
    headers:{
      "Content-Type": "application/json"
    },
    body: JSON.stringify(sound)
  })
  .then(response => response.text())
  .then(text => {
    console.log(text);
});
});
}

document.addEventListener('keydown',function(event){
  console.log(event.key)
  console.log(buttonValue)
  if (event.key==buttonValue){
    if(document.querySelector('#DocumentData')){
      console.log('hello')
      RecordRequestDoc()
}
  }
});

document.addEventListener('keydown',function(event){
  console.log(event.key)
  console.log(StopbuttonValue)
  if (event.key==StopbuttonValue){
    if(document.querySelector('#DocumentData')){
    console.log('hello')
    StopRequestDoc()
}
  }
});
window.clicked=false
  function Clicked(){
    console.log("gello")
    window.clicked=true
    document.addEventListener('keyup',function(){
    entering()
    })
  }


function entering(){
  console.log('yes')
  if(document.querySelector("#DocumentData")){
    let Data=document.getElementById("DocumentData").innerHTML
    fetch('/getData',{
      method : "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify(Data)
    })
    .then(response => response.text())
    .then(text => {
      console.log(text);
  });
}}

function paused(){
  var Data=""
    fetch('/recordPause',{
      method : "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify(Data)
    })
    .then(response => response.text())
    .then(text => {
      console.log(text);
  });
}

function ear(){
  var Data=""
    fetch('/recordEar',{
      method : "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify(Data)
    })
    .then(response => response.text())
    .then(text => {
      console.log(text);
  });
}

