


function validar(){
	document.getElementById('submit').style.display='none';

}
function delivery(){
    document.getElementById('id_numero').style.display='block ';
	document.getElementById('deli').style.display='none';
	document.getElementById('paraLlevar').style.margin='1rem';
	document.getElementById('paraLlevar2').style.margin='1rem';
	document.getElementById('id_valNombre').value=1;
	document.getElementById('id_valMesa').value=0;
	document.getElementById('anuncio').style.display='none';
	document.getElementById('paraLlevar').style.display='none';
	document.getElementById('id_direccion').style.display='block';
	document.getElementById('paraLlevar2').style.display='none';
	document.getElementById('id_check2').click();
	document.getElementById('id_nombre').style.display='block';
	document.getElementById('llevar').style.display='none';
	document.getElementById('aqui').style.display='none';
	document.getElementById('cambio').style.display='block';
	document.getElementById('submit').style.display='none';
	document.getElementById('comerAqui').style.display='none';
}


function aqui()
{
document.getElementById('id_valNombre').value=0;
document.getElementById('id_valMesa').value=1;
document.getElementById('anuncio').style.display='none';
document.getElementById('comerAqui').style.display='block';
document.getElementById('comerAqui2').style.display='block';
document.getElementById('id_mesa').style.display='block';
document.getElementById('id_mesa').style.display='block';
document.getElementById('llevar').style.display='none';
document.getElementById('aqui').style.display='none';
document.getElementById('deli').style.display='none';
document.getElementById('cambio').style.display='block';
conteo=document.getElementById('conteo').value;
if(conteo==0){
	document.getElementById('submit').style.display='none';
	document.getElementById('id_mesa').style.display='none';
	document.getElementById('comerAqui').style.display='block';
	document.getElementById('noMesas').style.display='block';
}else{
	document.getElementById('noMesas').style.display='none';
	document.getElementById('submit').style.display='none';
	document.getElementById('id_mesa').style.display='block';
	document.getElementById('comerAqui').style.display='block';

}

document.getElementById('cambio').style.alignContent='center';
document.getElementById('inicializar').style.width='300px';
}

function llevar() 
{
document.getElementById('deli').style.display='none';
document.getElementById('paraLlevar').style.margin='1rem';
document.getElementById('paraLlevar2').style.margin='1rem';
document.getElementById('id_valNombre').value=1;
document.getElementById('id_valMesa').value=0;
document.getElementById('anuncio').style.display='none';
document.getElementById('paraLlevar').style.display='block';
document.getElementById('paraLlevar2').style.display='none';
document.getElementById('id_check').click();
document.getElementById('id_nombre').style.display='block';
document.getElementById('llevar').style.display='none';
document.getElementById('aqui').style.display='none';
document.getElementById('cambio').style.display='block';
document.getElementById('submit').style.display='none';
document.getElementById('comerAqui').style.display='none';
}

document.addEventListener('DOMContentLoaded',
function ()
{

document.getElementById('noMesas').style.display='none';
document.getElementById('delivery').style.display='none';
document.getElementById('deli2').style.display='none';
document.getElementById('id_valNombre').value=0;
document.getElementById('id_valMesa').value=0;
document.getElementById('conteo').style.display='none';

document.getElementById('cambio').addEventListener('click',cambio,false);
document.getElementById('llevar').addEventListener('click',llevar,false);
document.getElementById('deli').addEventListener('click',delivery,false);
document.getElementById('aqui').addEventListener('click',aqui,false);

document.getElementById('id_mesa').addEventListener('click',magia,false);
document.getElementById('id_nombre').addEventListener('click',magia,false);

},false);

function magia(){
	document.getElementById('submit').style.display='block';
	document.getElementById('id_meseros').style.display='block';
}