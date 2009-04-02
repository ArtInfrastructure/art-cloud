function baseInit(){
	$("#search-form").hide();
	$("#add-installation-photo-widget").hide();
}
$(document).ready(function() { baseInit(); });

function showAddInstallationPhotoWidget() {
	$("#add-installation-photo-widget").show();
}
function hideAddInstallationPhotoWidget() {
	$("#add-installation-photo-widget").hide();
}