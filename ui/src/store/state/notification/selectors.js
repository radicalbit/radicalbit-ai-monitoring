const selectNotificationMessage = ({ notification: { message } }) => message;
const selectNotificationShowMessage = ({ notification: { showMessage } }) => showMessage;
const selectNotificationBox = ({ notification: { box } }) => box;
const selectNotificationShowBox = ({ notification: { showBox } }) => showBox;

export default {
  selectNotificationMessage,
  selectNotificationShowMessage,
  selectNotificationBox,
  selectNotificationShowBox,
};
