from datetime import datetime
import unittest
import uuid

from app.models.traces.tracing_dto import TraceDTO


class TracingDTOTest(unittest.TestCase):
    def test_convert_traces_to_dto(self):
        # Arrange
        traces = [
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:26:02.186871'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '6fd4061cad7dd30d',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 732713,
                'parent_span_id': '81422d395ebd6d20',
                'span_name': 'ChannelWrite<...,agent>.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.931849'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '12dd1faee87eadaf',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 600514,
                'parent_span_id': 'cd39d8df80ca89e1',
                'span_name': 'ChannelWrite<...>.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.933867'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '1b2aa4bbe33ec0f3',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 589038,
                'parent_span_id': 'cd39d8df80ca89e1',
                'span_name': 'ChannelWrite<start:agent>.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.923741'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': 'd2b0ad58fd7549e1',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 3291031789,
                'parent_span_id': '',
                'span_name': 'LangGraph.workflow',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.929725'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': 'cd39d8df80ca89e1',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 5059005,
                'parent_span_id': 'd2b0ad58fd7549e1',
                'span_name': '__start__.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.938564'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '81422d395ebd6d20',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 3251647366,
                'parent_span_id': 'd2b0ad58fd7549e1',
                'span_name': 'agent.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:26:02.191696'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '048e2176168294cf',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 4802592,
                'parent_span_id': 'd2b0ad58fd7549e1',
                'span_name': 'ask_human.task',
                'status_code': 'Error',
                'events_attributes': [
                    {
                        'exception.escaped': 'False',
                        'exception.message': "(Interrupt(value='Where do you want to search?', resumable=True, ns=['ask_human:443faf8d-e8d1-5fc2-2b17-a7b7c36eeda3'], when='during'),)",
                        'exception.stacktrace': 'Traceback (most recent call last):\n  File "/usr/local/lib/python3.11/site-packages/langgraph/utils/runnable.py", line 546, in invoke\n    input = step.invoke(input, config, **kwargs)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "/usr/local/lib/python3.11/site-packages/langgraph/utils/runnable.py", line 310, in invoke\n    ret = context.run(self.func, *args, **kwargs)\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "/usr/local/lib/python3.11/site-packages/agent/utils/nodes.py", line 50, in ask_human\n    location = interrupt(\'Where do you want to search?\')\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "/usr/local/lib/python3.11/site-packages/langgraph/types.py", line 490, in interrupt\n    raise GraphInterrupt(\nlanggraph.errors.GraphInterrupt: (Interrupt(value=\'Where do you want to search?\', resumable=True, ns=[\'ask_human:443faf8d-e8d1-5fc2-2b17-a7b7c36eeda3\'], when=\'during\'),)\n',
                        'exception.type': 'langgraph.errors.GraphInterrupt',
                    }
                ],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:26:02.188588'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '57646f608c71ec17',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 741633,
                'parent_span_id': '81422d395ebd6d20',
                'span_name': 'should_continue.task',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '',
                'prompt_tokens': '',
                'total_tokens': '',
            },
            {
                'created_at': datetime.fromisoformat('2025-03-12 15:25:58.940913'),
                'trace_id': '7b5f4662b860e3af14600cbb580497f5',
                'span_id': '552a4521e2e47801',
                'project_uuid': '00000000-0000-0000-0000-000000000003',
                'duration': 3244985058,
                'parent_span_id': '81422d395ebd6d20',
                'span_name': 'smart-model-langgraph-app_00000000-0000-0000-0000-000000000003.chat',
                'status_code': 'Unset',
                'events_attributes': [],
                'session_uuid': '00000000-0000-0000-0000-000000000092',
                'completion_tokens': '32',
                'prompt_tokens': '177',
                'total_tokens': '209',
            },
        ]

        project_uuid = uuid.UUID('00000000-0000-0000-0000-000000000003')

        # Act
        result = TraceDTO.convert_traces_to_dto(traces, project_uuid)

        # Assert
        assert isinstance(result, TraceDTO)
        assert result.project_uuid == project_uuid
        assert result.trace_id == '7b5f4662b860e3af14600cbb580497f5'
        assert result.span_id == 'd2b0ad58fd7549e1'
        assert result.session_uuid == uuid.UUID('00000000-0000-0000-0000-000000000092')
        assert result.spans == 9
        assert result.duration == 3291031789
        assert result.completion_tokens == 32
        assert result.prompt_tokens == 177
        assert result.total_tokens == 209
        assert result.number_of_errors == 1  # From the exception in ask_human.task
        assert result.created_at == '2025-03-12 15:25:58.923741'
        assert result.latest_span_ts == '2025-03-12 15:26:02.191696'

        # Verify tree structure
        assert result.tree.span_name == 'LangGraph.workflow'

        # The root should have 3 children
        assert len(result.tree.children) == 3

        # Find the __start__ node and verify its children
        start_node = next(
            (
                node
                for node in result.tree.children
                if node.span_name == '__start__.task'
            ),
            None,
        )
        assert start_node is not None
        assert len(start_node.children) == 2

        # Find the agent node and verify its children
        agent_node = next(
            (node for node in result.tree.children if node.span_name == 'agent.task'),
            None,
        )
        assert agent_node is not None
        assert len(agent_node.children) == 3

        # Verify one of the leaf nodes
        channel_write_node = next(
            (
                node
                for node in agent_node.children
                if node.span_name == 'ChannelWrite<...,agent>.task'
            ),
            None,
        )
        assert channel_write_node is not None
        assert len(channel_write_node.children) == 0  # Should be a leaf node
