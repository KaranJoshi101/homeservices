class n{
  constructor(rating,freq){
    this.rating=rating;
    this.freq=freq;
  }
}
const ratings=document.querySelector('#ratings');
if(ratings){
  const rtx=document.querySelector('#rtx');
  
  
  let rec=[];
  for(let i=0;i<ratings.children.length;i++){
      rec.push(new n(ratings.children[i].id,ratings.children[i].innerText));
  }
  
  let xValues=[];
  let yValues=[];
  for(let i of rec){
      xValues.push(i.rating);
      yValues.push(i.freq);
  }
  
  
  var barColors=["#06C","#C9190B","#EF9234","#4CB140","#009596","#5752D1","#F4C145","#EC7A08","#7D1007","#B8BBBE"].slice(0,xValues.length);
  new Chart("rtx", {
  type: "doughnut",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      responsive: false,
      maintainAspectRatio: true
    }
  }
  });
  
}

const requests=document.querySelector('#requests');
const rqx=document.querySelector('#rqx');
rec=[];
for(let i=0;i<requests.children.length;i++){
    rec.push(new n(requests.children[i].id,requests.children[i].innerText));
}

xValues=[];
yValues=[];
for(let i of rec){
    xValues.push(i.rating);
    yValues.push(i.freq);
}

barColors=["#06C","#C9190B","#EF9234","#4CB140","#009596","#5752D1","#F4C145","#EC7A08","#7D1007","#B8BBBE"].slice(0,xValues.length);
new Chart("rqx", {
type: "bar",
data: {
  labels: xValues,
  datasets: [{
    backgroundColor: barColors,
    data: yValues
  }]
},
options: {
  title: {
    display: true,
    responsive: false,
    maintainAspectRatio: true
  },
  scales: {
    y: {
        beginAtZero: true
    }
}
}
});

const professionals=document.querySelector('#professionals');
if(professionals){
  const stx=document.querySelector('#stx');



rec=[];
for(let i=0;i<professionals.children.length;i++){
    rec.push(new n(professionals.children[i].id,professionals.children[i].innerText));
}

xValues=[];
yValues=[];
for(let i of rec){
    xValues.push(i.rating);
    yValues.push(i.freq);
}


barColors=["#06C","#C9190B","#EF9234","#4CB140","#009596","#5752D1","#F4C145","#EC7A08","#7D1007","#B8BBBE"].slice(0,xValues.length);
new Chart("stx", {
type: "bar",
data: {
  labels: xValues,
  datasets: [{
    backgroundColor: barColors,
    data: yValues
  }]
},
options: {
  title: {
    display: true,
    responsive: false,
    maintainAspectRatio: true
  }
}
});


}
