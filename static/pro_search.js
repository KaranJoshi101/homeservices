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
records=document.querySelectorAll('.records')
select=document.querySelector('#select')
search=document.querySelector('#search')
search.placeholder="Enter "+select.value + " Details"
select.addEventListener("click",()=>{
    search.placeholder="Enter "+select.value + " Details"

    

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