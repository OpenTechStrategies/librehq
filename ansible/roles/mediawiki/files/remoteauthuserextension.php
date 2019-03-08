<?php
wfLoadExtension( 'Auth_remoteuser' );

$wgAuthRemoteuserUserName = function() {
  return $_COOKIE["librehq_user"];
};
?>
