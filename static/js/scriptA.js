 function incrementar() {
valor = document.getElementById("id_cantidad");
extra = document.getElementById("id_cebolla")
if(extra==null){
extra=0;
}
valor.value++;
}
function decrementar() {
valor = document.getElementById("id_cantidad");
cond = document.getElementById("id_cebolla");
if (valor.value>=2)valor.value--;
if (cond.value>valor.value)cond.value=valor.value;
}
function incrementar1() {
total=document.getElementById("id_cantidad");
valor = document.getElementById("id_cebolla");
if(total.value>valor.value){
valor.value++;
}}
function decrementar1() {
valor = document.getElementById("id_cebolla");
if (valor.value>=1)
valor.value--;
}
function incrementar2() {
total=document.getElementById("id_cantidad");
valor = document.getElementById("id_aguacate");
if(total.value>valor.value){
valor.value++;
}}
function decrementar2() {
valor = document.getElementById("id_aguacate");
if (valor.value>=1)
valor.value--;
}
function incrementar3() {
    total=document.getElementById("id_cantidad");
    valor = document.getElementById("id_cebollaBase");
    if(total.value>valor.value){
    valor.value++;
    }}
    function decrementar3() {
    valor = document.getElementById("id_cebollaBase");
    if (valor.value>=1)
    valor.value--;
    }


document.addEventListener('DOMContentLoaded',
function ()
{
    document.getElementById('mostrarExtra').addEventListener('click',extras,false);
    if(document.getElementById("cebo")=="False"){
        document.getElementById('id_cebolla').style.display='none';
    }
    if(document.getElementById('agua')=='False'){
        document.getElementById('id_aguacate').style.display='none';
    }
},false);

function extrasMostrarC(){
document.getElementById('CExtraMas').style.display='block';
document.getElementById('CExtraMenos').style.display='block';
document.getElementById('id_cebolla').style.display='block';
document.getElementById('FC').style.display='block';
document.getElementById('TC').style.display='block';
}

function extrasMostrarA(){
document.getElementById('AExtraMas').style.display='block';
document.getElementById('AExtraMenos').style.display='block';
document.getElementById('id_aguacate').style.display='block';
document.getElementById('FA').style.display='block';
document.getElementById('TA').style.display='block';
}

function extrasMostrar2(){
document.getElementById('CExtraMas').style.display='block';
document.getElementById('CExtraMenos').style.display='block';
document.getElementById('AExtraMas').style.display='block';
document.getElementById('AExtraMenos').style.display='block';
document.getElementById('id_cebolla').style.display='block';
document.getElementById('id_aguacate').style.display='block';
document.getElementById('FC').style.display='block';
document.getElementById('TC').style.display='block';
document.getElementById('FA').style.display='block';
document.getElementById('TA').style.display='block';
}