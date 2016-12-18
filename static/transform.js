$( function () {

  $( "#srcWord" ).keydown( function(e) {
    if( e.which === 13 ) {
      $( "#transform" ).click();
    }
  });

  $( "#transform" ).click( function() {
    var srcWord = $( "#srcWord" ).val()
    var url = "/transform/es/en/" + srcWord;  
    
    $( "#status-text" ).text( "" );
    $( "#loading" ).show();
    
    var jqxhr = $.ajax( url )
      .done(function( data ) {
        if ( srcWord.toLowerCase() == data.translatedWord.toLowerCase() ) {
          $( "#status-text" ).text( "Translation not found");
          return;
        }

        if ( data.similarPhoneticWord.length == 0 ) {
          $( "#status-text" ).text( "Similar Phonetic not found");
          return;
        }

        $( "#translatedWord" ).text( data.translatedWord );
        $( "#similarPhoneticWord" ).text( data.similarPhoneticWord[0] );

      }).
      fail(function() {
        $( "#status-text" ).text( "Error. Try again");
      }).    
      always(function() {
        $( "#loading" ).hide();
      });
  });
    
});