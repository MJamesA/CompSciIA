(function($) {
   // Show modal when attempting to leave the page
  window.onbeforeunload = function(event) {
    // Show the modal
    $('#leaveModal').modal('show');
    
    // Prevent the default action of the event
    event.preventDefault();
    
   
  };

  // Handle the confirmation button
  $('#confirmLeave').onclick = function() {
    // Disable the warning
    window.onbeforeunload = null; 
    // Redirect to the desired URL
    window.location.href = '/'; // Specify the URL to redirect to
  };


})(jQuery);