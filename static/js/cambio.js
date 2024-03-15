document.addEventListener('DOMContentLoaded',
function ()
{
	document.getElementById('recibido').addEventListener('onInput',calcular,false);
},false);

function calcular{
	document.getElementById('tablepe').style.display='none';
	document.getElementById('cambio').value=document.getElementById('recibido').value-document.getElementById('cobro').value;
}