import { Drawer } from "@radicalbit/radicalbit-design-system"
import { useSearchParams } from "react-router-dom";
import TreeComponent from "./tree";

const TraceDetailDrawer = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const traceDetailOpened = searchParams.get('trace-detail');
  const traceDetailExpanded = searchParams.get('trace-detail-expanded');

  const handleOnClose = () => {
    searchParams.delete('trace-detail');
    searchParams.delete('trace-detail-expanded');
    setSearchParams(searchParams)
  }

  const drawerWidth = traceDetailExpanded ? "50%" : "25%"

  return (
    <Drawer
      width={drawerWidth}
      mask={false}
      onClose={handleOnClose}
      open={traceDetailOpened ? true : false}
    >
      <div className="flex flex-row gap-2">
        <TreeComponent />
        {traceDetailExpanded && <TraceDetail />}

      </div>
    </Drawer>
  )
}

const TraceDetail = () => {
  return <span>Trace Detail</span>
}



export default TraceDetailDrawer