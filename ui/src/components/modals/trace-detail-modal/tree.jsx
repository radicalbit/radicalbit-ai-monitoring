import { Spinner } from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { Tree } from 'antd';
import { useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';

const { useGetTraceDetailByUUIDQuery } = tracingApiSlice;

function TreeComponent() {
  const { uuid: projectUuid } = useParams();

  const [searchParams, setSearchParams] = useSearchParams();
  const traceUuid = searchParams.get('traceUuid');
  const expandedKey = searchParams.get('expandedKey') ?? '0-0';

  const { data, isLoading, isError } = useGetTraceDetailByUUIDQuery({ projectUuid, traceUuid });
  const treeData = [mapTree(data?.tree)];

  useEffect(() => {
    searchParams.set('expandedKey', '0-0');
    setSearchParams(searchParams);
  }, [searchParams, setSearchParams]);

  const onSelect = (_, info) => {
    searchParams.set('expandedKey', info.node.key);
    searchParams.set('spanId', info.node.spanId);
    setSearchParams(searchParams);
  };

  if (isLoading || isError) {
    return <Spinner />;
  }

  if (treeData?.length === 0) {
    return 'No data';
  }

  return (
    <Tree
      className="bg-transparent min-w-[30rem]"
      defaultExpandedKeys={[expandedKey]}
      onSelect={onSelect}
      showLine
      treeData={treeData}
    />
  );
}

function mapTree(node, parentKey = '0') {
  if (!node) return [];

  const lastElement = parentKey.split('-').splice(-1);

  const currentKey = parentKey.length === 1 ? '0-0' : `${parentKey}-${parseInt(lastElement, 10) + 1}`;

  const errorStyle = node.numberOfErrors > 0 ? 'text-red-500' : '';

  const mappedNode = {
    title: () => (
      <div className="flex flex-col">

        <div className={`${errorStyle}`}>{node.spanName}</div>

        <small>
          {numberFormatter().format(node.durationsMs / 1000)}
          s
        </small>

      </div>
    ),
    key: currentKey,
    spanId: node.spanId,
    children: [],
  };

  if (node.children && node.children.length > 0) {
    mappedNode.children = node.children.map((child, index) => mapTree(child, `${parentKey}-${index}`));
  }

  return mappedNode;
}

export default TreeComponent;
