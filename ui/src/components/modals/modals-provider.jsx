import { ModalsEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import AddNewApiKeyModal from './add-new-api-key';
import AddNewModel from './add-new-model';
import AddNewProjectModal from './add-new-project';
import CompletionImportDetailModal from './completion-import-detail-modal';
import CurrentImportsDetailModal from './current-import-detail-modal';
import TraceDetailModal from './trace-detail-modal';
import EditProjectModal from './edit-project';

export default function ModalsProvider() {
  const { modalPayload: { modalName } } = useModals();

  switch (modalName) {
    case ModalsEnum.ADD_NEW_MODEL:
      return <AddNewModel />;

    case ModalsEnum.CURRENT_IMPORT_DETAIL:
      return <CurrentImportsDetailModal />;

    case ModalsEnum.COMPLETION_IMPORT_DETAIL:
      return <CompletionImportDetailModal />;

    case ModalsEnum.ADD_NEW_PROJECT:
      return <AddNewProjectModal />;

    case ModalsEnum.EDIT_PROJECT:
      return <EditProjectModal />;

    case ModalsEnum.TRACE_DETAIL:
      return <TraceDetailModal />;

    case ModalsEnum.ADD_NEW_API_KEY:
      return <AddNewApiKeyModal />;

    default:
      return false;
  }
}
