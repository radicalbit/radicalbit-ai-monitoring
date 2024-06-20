import { DefaultTitle, NotificationEnum } from '@State/notification/constants';

export const isGenericError = (e) => typeof e === 'object' && e !== null && 'message' in e;

export const notificationErrorJson = (e) => {
  if (!isGenericError(e)) {
    return {
      type: NotificationEnum.ERROR,
      title: DefaultTitle.ERROR,
      content: `Unknown ${DefaultTitle.ERROR.toLowerCase()}`,
    };
  }

  const titleStatus = e.status ? `${e.status}` : '';
  const titleStatusText = e.statusText ? `${e.statusText}` : DefaultTitle.ERROR;
  const title = `${titleStatus} ${titleStatusText}`;

  return { type: NotificationEnum.ERROR, title, content: e.message };
};

export const notificationSuccessJson = (
  title = DefaultTitle.SUCCESS,
  content = DefaultTitle.SUCCESS.toLowerCase(),
) => ({ type: NotificationEnum.SUCCESS, title, content });

export const notificationWarningJson = (
  title = DefaultTitle.WARNING,
  content = DefaultTitle.WARNING.toLowerCase(),
) => ({ type: NotificationEnum.WARNING, title, content });
