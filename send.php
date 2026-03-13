<?php
/**
 * Ин файл маълумотро аз формаи HTML мегирад ва 
 * тавассути Telegram Bot API ба шумо мефиристад.
 */

// --- ТАНЗИМОТ (МАЪЛУМОТИ ХУДРО ИН ҶО ГУЗОРЕД) ---
$token = "ТОКЕНИ_АЗ_BOTFATHER_ГИРИФТА"; // Масалан: "723456789:AAHeR..."
$chat_id = "ID_И_АЗ_USERINFOBOT_ГИРИФТА"; // Масалан: "556677889"

// ------------------------------------------------

// Санҷиши он ки оё маълумот тавассути POST омадааст
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // 1. Гирифтани маълумот аз майдонҳои форма
    // 'name', 'phone', 'method' ва 'comment' бояд дар HTML-и шумо дар аттрибути name="" бошанд
    $userName    = strip_tags($_POST['name']);
    $userPhone   = strip_tags($_POST['phone']);
    $orderMethod = strip_tags($_POST['method']);
    $orderText   = strip_tags($_POST['comment']);

    // 2. Омода кардани матни паём барои Telegram
    // Мо тегҳои HTML-ро барои зебо нишон додани матн истифода мебарем
    $message  = "<b>🔔 ФАРМОИШИ НАВ ДАР САЙТ!</b>\n\n";
    $message .= "<b>👤 Муштарӣ:</b> " . $userName . "\n";
    $message .= "<b>📞 Телефон:</b> " . $userPhone . "\n";
    $message .= "<b>🚚 Усул:</b> " . $orderMethod . "\n";
    $message .= "<b>📝 Тафсилот:</b>\n" . $orderText;

    // 3. Параметрҳо барои фиристодан
    $params = [
        'chat_id' => $chat_id,
        'text' => $message,
        'parse_mode' => 'html' // Барои он ки тегҳои <b> кор кунанд
    ];

    // 4. Истифодаи cURL барои фиристодани паём ба Telegram
    $url = "https://api.telegram.org/bot{$token}/sendMessage";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Барои пешгирии хатогиҳои SSL дар баъзе хостингҳо

    $result = curl_exec($ch);
    $error = curl_error($ch);
    curl_close($ch);

    // 5. Натиҷа
    if ($result) {
        // Агар бомуваффақият равад, ба саҳифаи асосӣ мебарем ва хабар медиҳем
        header('Location: index.html?status=success#order');
        exit;
    } else {
        // Агар хатогӣ шавад
        echo "Хатогӣ ҳангоми фиристодан: " . $error;
    }
} else {
    // Агар касе мустақиман ба ин файл дарояд, иҷозат намедиҳем
    echo "Иҷозат нест!";
}
?>
