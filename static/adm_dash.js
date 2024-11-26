let servBtn=document.querySelectorAll('.servBtn');
let proBtn=document.querySelectorAll('.proBtn');
Category=document.querySelector('#Category');

let probackbtn=document.querySelectorAll('.proback');
let servbackbtn=document.querySelectorAll('.servback');
let l=[];
for(let c of servBtn){
    c.addEventListener("click",()=>{
        Category.style.display="none";
        try{
            let servcat=document.getElementById(`serv${c.value}`);
            servcat.style.display="block";
            l.push(servcat);
        }
        catch(exp){

        }
        
    })
}
for(let c of proBtn){
    c.addEventListener("click",()=>{
        Category.style.display="none";
        try{
            let pro=document.getElementById(`pro${c.value}`);
            pro.style.display="block";
            l.push(pro);
        }
        catch(exp){

        }
        
    })
}
for(let back of servbackbtn){
    back.addEventListener("click",()=>{
        Category.style.display="block";
        if(l.length){
            servcat=l.pop()
            servcat.style.display="none";
        }
        
    })
}
for(let back of probackbtn){
    back.addEventListener("click",()=>{
        Category.style.display="block";
        if(l.length){
            pro=l.pop()
            pro.style.display="none";
        }
        
    })
}