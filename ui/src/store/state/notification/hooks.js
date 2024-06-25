import { Message } from '@radicalbit/radicalbit-design-system';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { actions as notificationActions, selectors as notificationSelectors } from '@State/notification';

const { selectNotificationMessage, selectNotificationShowMessage } = notificationSelectors;
const { resetNotificationMessage } = notificationActions;

const useNotification = () => {
  const dispatch = useDispatch();
  const notificationMessage = useSelector(selectNotificationMessage);
  const notificationShowMessage = useSelector(selectNotificationShowMessage);

  useEffect(() => {
    if (notificationShowMessage) {
      const { type, title, content } = notificationMessage;
      Message[type]({ title, content });

      dispatch(resetNotificationMessage());
    }
  }, [dispatch, notificationMessage, notificationShowMessage]);
};

export { useNotification };
