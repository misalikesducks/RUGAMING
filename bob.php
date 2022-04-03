<?php
require_once 'vendor/autoload.php'
use Twilio\TwiML\MessagingResponse;
$response = new MessagingResponse();
$response ->message("It works! @Vinix Code");
print $response;