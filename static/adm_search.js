function check(str){
    str=str.toLowerCase()
    newstr=''
    for(s of str){
        if(s==' '){
            continue;
        }
        newstr+=s
    }
    return newstr
}
msg=document.querySelector('#msg')
const list={'Category':document.querySelector("#Category"),'Service':document.querySelector("#Service"),'Professional':document.querySelector("#Professional"),'Customer':document.querySelector("#Customer"),'Request':document.querySelector("#Request")}
var records=document.querySelectorAll(`.${select.value}`)
var table=document.querySelector(`#${select.value}`)
table.style.display='block';
select=document.querySelector('#select');
search=document.querySelector('#search')
search.placeholder="Enter "+select.value + " Details"
select.addEventListener("click",()=>{
    search.placeholder="Enter "+select.value + " Details"
    table.style.display='none';
    table=document.querySelector(`#${select.value}`)
    table.style.display='block';

    records=document.querySelectorAll(`.${select.value}`)

})

search.addEventListener('keyup',()=>{
    
    let srh=check(search.value)
    found=false;
    for(rec of records){
       
        if(check(rec.id).includes(srh)){
           
            rec.style.display='';
            found=true;
        }
        else{
            rec.style.display='none';
        }
    }
    if(!found){
        msg.style.display='';
    }
    else{
        msg.style.display='none';
    }
})