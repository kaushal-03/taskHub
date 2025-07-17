const axios = require('axios');

// Function to send Expo push notification
async function sendExpoPushNotification(expoPushToken) {
  const message = {
    to: expoPushToken,
    sound: 'default',
    title: 'Hello!',
    body: 'You recieved a mail from the selected sender',
  };

  try {
    const response = await axios.post('https://exp.host/--/api/v2/push/send', message);
    console.log('Notification sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending notification:', error);
  }
}

// Example Expo push token (replace this with your actual token)
const expoPushToken = 'ExponentPushToken[jbmZWyMQxzLgNospP0L4GT]';
sendExpoPushNotification(expoPushToken);
