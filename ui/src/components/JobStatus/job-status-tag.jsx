import { JOB_STATUS } from '@Src/constants';
import { Tag } from '@radicalbit/radicalbit-design-system';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useParams } from 'react-router';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

function JobStatusTag() {
  const { uuid } = useParams();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const jobStatus = data?.jobStatus;

  switch (jobStatus) {
    case JOB_STATUS.IMPORTING: {
      return (
        <Tag type="dashed-secondary">{JOB_STATUS.IMPORTING}</Tag>
      );
    }

    case JOB_STATUS.ERROR: {
      return (
        <Tag type="error-light">{JOB_STATUS.ERROR}</Tag>
      );
    }

    case JOB_STATUS.MISSING_REFERENCE: {
      return false;
    }

    default: return false;
  }
}

export default JobStatusTag;
