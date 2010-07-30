function baseInit(){
	$("#search-form").hide();
	$("#add-installation-photo-widget").hide();
	$("#add-installation-document-widget").hide();
}
$(document).ready(function() { baseInit(); });

function showAddInstallationPhotoWidget() {
	$("#add-installation-photo-widget").show();
}
function hideAddInstallationPhotoWidget() {
	$("#add-installation-photo-widget").hide();
}

function showAddInstallationDocumentWidget() {
	$("#add-installation-document-widget").show();
}
function hideAddInstallationDocumentWidget() {
	$("#add-installation-document-widget").hide();
}