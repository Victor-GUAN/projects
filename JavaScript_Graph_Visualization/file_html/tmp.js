/**
 * Created by MGN11 on 4/11/2017.
 */
 
document.getElementById('import').onclick = function(){
	
    var files = document.getElementById('selectFiles').files;
    /*console.log(files);*/
    if (files.length <= 0) {
        return false;
    }

	console.log(files.item(0))
	
    var fr = new FileReader();

    fr.onload = function(event) {
		
        console.log(event.target.result);
        var result = JSON.parse(event.target.result);
		console.log(result);
        var formatted = JSON.stringify(result, null, 2);

    };

    fr.readAsText(files.item(0));

};