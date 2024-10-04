var catBtn=document.querySelectorAll('.catBtn');
var categories=document.querySelector('#categories');

var backbtn=document.querySelectorAll('.back');
var l=[];
for(let c of catBtn){
    c.addEventListener("click",()=>{
        categories.style.display="none";
        try{
            console.log(c.value);
            let servcat=document.getElementById(`${c.value}`);
            console.dir(servcat);
            servcat.style.display="block";
            l.push(servcat);
        }
        catch(exp){

        }
        
    })
}
for(let back of backbtn){
    back.addEventListener("click",()=>{
        categories.style.display="block";
        if(l.length){
            servcat=l.pop()
            servcat.style.display="none";
        }
        
    })
}
