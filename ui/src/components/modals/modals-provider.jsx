import { ModalsEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import AddNewModel from './add-new-model';
import CurrentImportsDetailModal from './current-import-detail-modal';
import CompletionImportDetailModal from './completion-import-detail-modal';

export default function ModalsProvider() {
  const { modalPayload: { modalName } } = useModals();

  switch (modalName) {
    case ModalsEnum.ADD_NEW_MODEL:
      return <AddNewModel />;

    case ModalsEnum.CURRENT_IMPORT_DETAIL:
      return <CurrentImportsDetailModal />;

    case ModalsEnum.COMPLETION_IMPORT_DETAIL:
      return <CompletionImportDetailModal />;

    default:
      return false;
  }
}
