#!/usr/bin/env python3
"""Reproduce the editable SVG and its design records (Python standard library)."""
from pathlib import Path
from html import escape
import json
import argparse
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / 'inspection-agent-architecture.svg'
INK, BLUE, TEAL, PURPLE = '#142D59', '#2457A6', '#14645F', '#6650AD'
MUTED, BORDER = '#435875', '#8AA4D0'
parts, labels = [], []

def add(s): parts.append(s)
def text(x, y, value, size=22, color=INK, weight=400, anchor='start'):
    labels.append(value)
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')
def rect(x,y,w,h,fill='#FFFFFF',stroke=BORDER,r=16,dash=None):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def line(x1,y1,x2,y2,color=BORDER,width=1.4):
    add(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def path(d,color=INK,width=2.7,arrow=False,dash=False):
    marker = 'teal' if color==TEAL else 'purple' if color==PURPLE else 'blue'
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'+(f' marker-end="url(#{marker})"' if arrow else '')+(' stroke-dasharray="8 6"' if dash else '')+'/>')
def group(id): add(f'<g id="{id}">')
def end(): add('</g>')
def icon(kind,x,y,color=BLUE,scale=1):
    add(f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">')
    shapes={
      'route':'<path d="M4 42h14c13 0 13-16 0-16S7 10 19 10h13"/><path d="M37 9c-10 0-10 13 0 20 10-7 10-20 0-20Z"/><circle cx="37" cy="16" r="2.5"/>',
      'eye':'<path d="M2 25C13 7 37 7 48 25 37 43 13 43 2 25Z"/><circle cx="25" cy="25" r="8"/>',
      'compare':'<rect x="2" y="6" width="18" height="32" rx="3"/><rect x="30" y="6" width="18" height="32" rx="3"/><path d="M7 30l5-7 4 3M35 30l5-14 4 6M20 44h10m-3-3 3 3-3 3"/>',
      'report':'<path d="M10 2h23l9 10v36H10Z M32 3v11h10M17 23h18M17 30h18M17 37h11"/>',
      'tool':'<path d="M15 4v11l10 7 10-7V4M25 22v25M5 36h40"/><circle cx="25" cy="30" r="3"/>',
      'brain':'<path d="M25 8C17-1 8 7 10 14 0 18 4 31 10 31 6 42 19 49 25 39 31 49 44 42 40 31 48 31 50 18 40 14 42 7 33-1 25 8ZM25 8v31M12 19l7 5-6 6M38 19l-7 5 6 6"/>',
      'user':'<circle cx="25" cy="12" r="9"/><path d="M8 46v-9c0-16 34-16 34 0v9M17 37v9M33 37v9"/>',
      'camera':'<rect x="3" y="14" width="44" height="29" rx="6"/><path d="M13 14l4-8h16l4 8"/><circle cx="25" cy="28" r="9"/>',
      'radar':'<path d="M25 42V9M10 27a21 21 0 0 1 30 0M4 20a30 30 0 0 1 42 0M17 34a11 11 0 0 1 16 0"/><circle cx="25" cy="42" r="3"/>',
      'robot':'<rect x="10" y="9" width="30" height="21" rx="7"/><path d="M25 9V2M17 36h16l5 13M17 36l-5 13M25 30v18M6 14v12M44 14v12"/><circle cx="19" cy="19" r="2"/><circle cx="31" cy="19" r="2"/>',
      'shield':'<path d="M25 3 44 11v14c0 11-12 20-19 24C18 45 6 36 6 25V11ZM15 25l7 7 14-15"/>',
      'map':'<path d="M3 8l14-5 16 7 14-5v36l-14 5-16-7-14 5ZM17 3v36M33 10v36"/>',
      'episode':'<rect x="4" y="4" width="42" height="32" rx="5"/><path d="M10 44h30M17 12l15 9-15 9Z"/>',
      'schema':'<rect x="17" y="2" width="16" height="13" rx="3"/><rect x="1" y="35" width="16" height="13" rx="3"/><rect x="33" y="35" width="16" height="13" rx="3"/><path d="M25 15v10H9v10M25 25h16v10"/>',
    }
    add(shapes[kind]); end()

add('<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1920" height="1080" viewBox="0 0 1920 1080" role="img" aria-labelledby="title desc">')
add('<title id="title">记忆增强的巡检机器人 Agent：概念架构</title><desc id="desc">用户任务经由模型和 Harness 调度技能，技能通过机器人适配和安全控制执行。工作记忆连接在线运行与空间、情景、语义记忆。受检巩固形成规律，受控演化为后续扩展。</desc>')
add('<defs><linearGradient id="blueWash" x2="1" y2="1"><stop stop-color="#F7FAFF"/><stop offset="1" stop-color="#EAF1FF"/></linearGradient><linearGradient id="purpleWash" x2="1" y2="1"><stop stop-color="#FBFAFF"/><stop offset="1" stop-color="#F0ECFC"/></linearGradient><linearGradient id="mintWash" x2="1" y2="1"><stop stop-color="#F6FCFB"/><stop offset="1" stop-color="#E8F5F1"/></linearGradient>')
for name,col in [('blue',INK),('teal',TEAL),('purple',PURPLE)]:
    add(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1 9 5 1 9" fill="none" stroke="{col}" stroke-width="1.7" stroke-linejoin="round"/></marker>')
add('</defs><rect width="1920" height="1080" fill="#FFFFFF"/><g font-family="PingFang SC, Noto Sans CJK SC, Microsoft YaHei, Arial, sans-serif">')

# A restrained title occupies the otherwise unused corner, not the diagram body.
group('figure-heading')
text(40,88,'记忆增强的',30,weight=650)
text(40,132,'巡检机器人',30,weight=650)
text(40,176,'Agent',38,BLUE,700)
line(40,205,250,205,BLUE,2)
text(40,236,'概念架构 · 研究设计',20,MUTED)
end()

# Skills form the physical and digital capability boundary.
group('skills')
rect(330,40,1220,210,'url(#purpleWash)','#9B8DCB',22)
text(940,82,'技能与工具  Skills & Tools',30,weight=700,anchor='middle')
for i,(kind,title,detail) in enumerate([
    ('route','导航与重访','到达目标 · 调整视角'),
    ('eye','视觉感知','识别对象 · 读取状态'),
    ('compare','变化与异常核查','历史对比 · 规范核对'),
    ('report','巡检报告','异常摘要 · 证据引用'),
    ('tool','可扩展技能','按平台接入操作能力'),
]):
    x=350+i*238
    if i: line(x-9,112,x-9,223,'#CCC4E9',1)
    icon(kind,x+90,107,PURPLE,.8)
    text(x+115,179,title,24,weight=650,anchor='middle')
    text(x+115,213,detail,19,MUTED,anchor='middle')
end()

group('agent')
rect(330,320,1220,355,'url(#blueWash)',BORDER,22)
text(358,357,'巡检 Agent · 在线闭环',29,weight=700)
group('reasoner')
rect(355,380,280,164,'#F8FAFF','#829FD0')
icon('brain',375,396,BLUE,.75)
text(491,425,'VLM / LLM',27,weight=700,anchor='middle')
text(495,466,'场景理解 · 任务推理',22,anchor='middle')
text(495,505,'提出计划与工具调用',20,MUTED,anchor='middle')
end()
group('harness')
rect(700,380,825,164,'#E8F0FF','#829FD0')
text(1112,410,'Agent Harness · 运行编排',27,weight=700,anchor='middle')
for x,w,title,detail in [(718,245,'规划与调度','子目标 · 前置条件'),(988,245,'上下文管理','检索 · 压缩 · 预算'),(1258,249,'验证与恢复','证据验收 · 重试 / 停止')]:
    rect(x,428,w,96,'#FFFFFF','#A6B9D8',10)
    text(x+w/2,463,title,24,weight=600,anchor='middle')
    text(x+w/2,499,detail,19,MUTED,anchor='middle')
end()
path('M700 449H635',arrow=True); text(667,435,'调用',17,anchor='middle')
path('M635 508H700',arrow=True); text(667,493,'建议',17,anchor='middle')
group('working-memory')
rect(355,586,1170,64,'#FFFFFF','#829FD0',12)
text(378,626,'L1 工作记忆',25,BLUE,650)
line(554,600,554,638,'#B1C0D9')
text(581,626,'当前目标 / 进度    ·    近期观测 / 对象状态    ·    历史检索证据    ·    不确定性',21)
end()
path('M900 586V544',arrow=True); path('M1300 544V586',arrow=True)
text(1100,572,'构造上下文 / 更新任务状态',19,MUTED,anchor='middle')
end()

# Paired directed edges distinguish commands from grounded feedback.
group('online-edges')
path('M1085 380V250',arrow=True); text(1064,288,'技能调用',20,anchor='end')
path('M1330 250V380',arrow=True); text(1350,288,'结果与证据',20)
path('M265 423H330',arrow=True); text(297,406,'任务',18,anchor='middle')
path('M330 556H265',arrow=True); text(297,539,'报告',18,anchor='middle')
path('M1550 149H1630',arrow=True); text(1590,134,'指令',18,anchor='middle')
path('M1630 213H1550',arrow=True); text(1590,198,'观测',18,anchor='middle')
end()

group('user')
rect(35,320,230,355,'url(#blueWash)',BORDER,22)
icon('user',125,344,BLUE,.8)
text(150,420,'用户 / 运维人员',25,weight=650,anchor='middle')
line(56,443,244,443,'#B9C8DF')
text(150,480,'任务目标与约束',22,anchor='middle')
text(150,515,'巡检范围 · 安全规范',19,MUTED,anchor='middle')
text(150,577,'结果与证据回传',22,anchor='middle')
text(150,612,'必要时确认 / 接管',19,MUTED,anchor='middle')
end()

group('hardware')
rect(1630,40,255,635,'url(#blueWash)',BORDER,22)
text(1757,84,'机器人执行层',28,weight=700,anchor='middle')
text(1757,116,'Robot & Environment',18,MUTED,anchor='middle')
rect(1647,138,220,91,'#FFFFFF','#A5B8D6',12)
text(1757,173,'平台适配接口',24,weight=600,anchor='middle')
text(1757,207,'指令分发 · 状态回传',19,MUTED,anchor='middle')
icon('camera',1661,255,BLUE,.72)
text(1716,278,'相机 / RGB-D',23,weight=600)
text(1716,307,'图像 · 深度',19,MUTED)
icon('radar',1661,338,BLUE,.72)
text(1716,362,'LiDAR / IMU',23,weight=600)
text(1716,391,'几何 · 位姿',19,MUTED)
icon('robot',1661,421,BLUE,.72)
text(1716,446,'运动与执行器',23,weight=600)
text(1716,475,'低层闭环控制',19,MUTED)
rect(1647,509,220,99,'#F0F3F9','#869BB9',12)
icon('shield',1660,531,INK,.62)
text(1765,548,'独立安全控制',22,weight=650,anchor='middle')
text(1757,582,'限速 · 避障 · 急停',20,anchor='middle')
text(1757,645,'感知环境 ↔ 执行动作',21,MUTED,anchor='middle')
end()

group('memory')
rect(330,755,1220,290,'url(#mintWash)','#83B3AC',22)
text(356,795,'长期记忆  Long-term Memory',29,TEAL,700)
text(1525,794,'跨巡检积累 · 按证据检索 · 按版本更新',21,TEAL,anchor='end')
group('spatial')
rect(355,829,260,151,'#FFFFFF','#8CB7B1',14)
icon('map',370,846,TEAL,.62)
text(417,870,'空间记忆',25,TEAL,650)
text(375,911,'地点 · 拓扑 · 实体锚点',20)
text(375,947,'跨层索引 / 跨次身份关联',18,MUTED)
end()
group('episodic')
rect(650,829,355,151,'#FFFFFF','#8CB7B1',14)
icon('episode',665,846,TEAL,.62)
text(712,870,'L2 情景记忆',25,TEAL,650)
text(670,911,'何时 · 何地 · 何物 · 发生何事',20)
text(670,947,'观测 / 动作 / 结果 + 原始证据',19,MUTED)
end()
group('semantic')
rect(1110,829,415,151,'#FFFFFF','#8CB7B1',14)
icon('schema',1125,846,TEAL,.62)
text(1172,870,'L3 语义与图式记忆',25,TEAL,650)
text(1130,911,'常态 · 条件规律 · 可复用流程',21)
text(1130,947,'适用范围 · 反例 · 置信度 · 版本',20,MUTED)
end()
path('M615 908H650',TEAL,2.5,True)
path('M1005 908H1110',TEAL,2.5,True)
text(1057,883,'受检巩固',19,TEAL,600,anchor='middle')
text(1057,942,'聚合 / 反例',17,TEAL,anchor='middle')
line(355,995,1525,995,'#ACCEC7')
text(355,1024,'共同契约：时间 · 空间 · 来源 · 观测质量 · 版本',20,TEAL)
text(1525,1024,'未观测 ≠ 正常；统计常态 ≠ 安全规范',20,TEAL,600,anchor='end')
end()

group('memory-edges')
path('M827 650V755',TEAL,2.8,True)
text(802,711,'筛选写入经历',21,TEAL,anchor='end')
path('M1400 755V650',TEAL,2.8,True)
text(1375,711,'按任务检索 / 证据回填',21,TEAL,anchor='end')
end()

group('future-evolution')
rect(1630,755,255,290,'#F9F7FD','#8D7CB4',20,'8 6')
text(1757,796,'受控演化',27,PURPLE,700,anchor='middle')
text(1757,827,'后续扩展',19,PURPLE,anchor='middle')
line(1650,845,1865,845,'#C8BFDB')
text(1757,881,'失败诊断 → 候选修改',20,anchor='middle')
text(1757,916,'离线验证 → 回归门禁',20,anchor='middle')
text(1757,951,'批准部署 → 监控回滚',20,anchor='middle')
text(1757,1008,'Harness / 记忆策略',20,PURPLE,anchor='middle')
end()
path('M1550 938H1630',PURPLE,2.4,True,True)
text(1590,922,'轨迹',18,PURPLE,anchor='middle')
path('M1690 755V711H1587V525H1550',PURPLE,2.4,True,True)
text(1750,703,'通过门禁后部署',19,PURPLE,anchor='middle')

group('legend')
text(40,800,'阅读图示',23,weight=650)
path('M42 833H88',arrow=True); text(101,840,'运行 / 记忆流',19)
path('M42 878H88',PURPLE,2.4,True,True); text(101,885,'后续演化流',19)
text(40,938,'当前重点：L1–L3',21,TEAL,650)
text(40,977,'模型与平台可替换',19,MUTED)
text(40,1012,'图示不代表已实现',19,MUTED)
end()
add('</g></svg>')
svg = '\n'.join(parts)

sources=[
 {'kind':'user_instruction','uri_or_path':str(HERE/'reference/user-sketch.png'),'evidence':'用户草图：用户—Agent（VLM、Harness）—技能—机器人，工作记忆连接空间/情景/语义长期记忆；授权结合已有规划审视并完善。'},
 {'kind':'paper_figure','uri_or_path':'https://arxiv.org/html/2607.10350v3#S2.F1','revision_or_page':'v3 Figure 1','evidence':'仅提取层叠中央区域、输入和硬件侧栏、淡蓝紫青色、细轮廓圆角、图标及双向连接的视觉语法。'},
 {'kind':'project_plan','uri_or_path':str(ROOT/'docs/plan/roadmap.md'),'evidence':'L1–L3 当前优先；受控演化需要验证、门禁、审批和回滚。'},
 {'kind':'research_proposal','uri_or_path':str(ROOT/'research/2026-09-07/l3-memory-consolidation-agent.md'),'evidence':'L2 经历与可回看证据；L3 聚合、反例检验、适用范围及版本；统计常态和规范规则独立。'},
 {'kind':'research_survey','uri_or_path':str(ROOT/'research/2026-09-17/agent-harness-evolution-survey.md'),'evidence':'区分在线适应、记忆积累及持久 Harness 演化；候选需独立验证。'},
]
components=[{'id':i,'label':n} for i,n in [('user','用户 / 运维人员'),('reasoner','VLM / LLM'),('harness','Agent Harness'),('skills','技能与工具'),('hardware','机器人执行层'),('working-memory','L1 工作记忆'),('memory','长期记忆'),('spatial','空间记忆'),('episodic','L2 情景记忆'),('semantic','L3 语义与图式记忆'),('future-evolution','受控演化')]]
edges=[]
def edge(a,b,label,kind='runtime'):
    edges.append({'from':a,'to':b,'label':label,'kind':kind,'direction':'forward'})
for a,b,l in [('user','harness','任务目标与约束'),('harness','user','报告与证据'),('harness','reasoner','调用'),('reasoner','harness','建议'),('harness','skills','技能调用'),('skills','harness','结果与证据'),('skills','hardware','指令'),('hardware','skills','观测'),('working-memory','harness','构造上下文'),('harness','working-memory','更新任务状态')]: edge(a,b,l)
for a,b,l in [('working-memory','episodic','筛选写入经历'),('memory','working-memory','按任务检索 / 证据回填'),('spatial','episodic','空间关联'),('episodic','semantic','受检巩固')]: edge(a,b,l,'memory')
edge('memory','future-evolution','历史轨迹','future'); edge('future-evolution','harness','通过门禁后部署','future')
grammar={'composition':'top skills, central model and harness with working-memory strip, lower long-term memory; input at left and physical platform at right', 'regions':'large rounded low-tint panels with one level of inner cards; horizontal 16:9 adaptation of the reference', 'marks':'editable geometric vector icons, no copied raster illustrations', 'strokes':'thin panel borders, dark arrows, paired directed runtime edges; dashed future extension', 'fills':'very light blue, violet and mint gradients on white; no heavy shadows', 'typography':'Chinese sans serif with short English module aliases; dark navy headings', 'color_roles':'blue online cognition, purple tools and future extension, teal memory', 'motifs':'route, eye, comparison, document, model, camera, robot, map, episode and schema', 'emphasis':'central online agent plus evidence-grounded long-term memory', 'avoid':['cloud/edge dual-model topology','private/common memory topology','model/vendor branding']}
spec={'schema':'academic-figure/FigureSpec@1','figure_id':'inspection-agent-architecture','plan_revision':'r1','sources':sources,'prompt':'Draw an editable 16:9 vector system diagram. Use layered pale blue, violet and mint rounded panels with dark navy type and geometric line icons. Place skills above the agent, long-term memory below, user on the left and robot execution on the right. Show evidence-grounded memory and a separately dashed future evolution loop. Preserve the declared topology and exact Chinese labels.','aspect_ratio':'16:9','final_width_mm':338.7,'visible_text':labels,'layout':{'composition':'layered_boundary','hero':'harness','reading_order':['user','reasoner','harness','skills','hardware','working-memory','memory','future-evolution'],'nesting_depth':2,'whitespace':'balanced'},'topology':{'components':components,'connections':edges,'groups':[{'id':'agent','component_ids':['reasoner','harness','working-memory']},{'id':'long-term','component_ids':['spatial','episodic','semantic']}],'authority_boundaries':['Model proposes; Harness dispatches and checks evidence.','Physical execution remains in platform skills and independent low-level safety control.','Statistical regularities cannot override externally supplied safety norms.','Future evolved configurations require independent validation and release approval.']},'style_profile':'reference-led','style_source':'reference','style_grammar':grammar,'semantic_color_roles':{'reasoning':BLUE,'memory':TEAL,'tools_and_future':PURPLE,'text':INK,'background':'#FFFFFF'},'reference_images':[str(HERE/'reference/abot-agentos-figure1.png'),str(HERE/'reference/user-sketch.png')],'must_not_claim':['已实现或已验证','已冻结模型、平台或部署位置','异常反复出现即可成为安全规范','空间记忆等于另一个认知层级'],'forbidden_connections':['reasoner -> low-level actuators','evolution candidate -> production without validation'],'negative_constraints':['no raster embeds','no text outlines; text stays editable','no claimed performance numbers','no mandatory cloud service'],'prompt_review':'waived','workspace_root':str(ROOT),'output_path':str(OUT)}
plan={'schema':'academic-figure/FigurePlan@1','source_revision':'2026-09-21-r1','venue':'学术汇报 / 16:9 screen','sources':sources,'figures':[{'figure_id':spec['figure_id'],'figure_type':'system architecture','communication_goal':'解释在线巡检、可追溯记忆与受控巩固如何闭环','claim_scope':['proposed design, not implementation or measured result'],'hero_element':'Agent Harness + L1–L3 memory','required_nodes':components,'required_connections':edges,'authority_boundaries':spec['topology']['authority_boundaries'],'secondary_context':['future controlled evolution'],'forbidden_claims':spec['must_not_claim'],'forbidden_connections':spec['forbidden_connections'],'aspect_ratio':'16:9','final_width_mm':338.7,'style_profile_hint':'reference-led','reference_assets':spec['reference_images'],'open_questions':['model, embodiment and quantitative thresholds remain unfrozen'],'confidence':'high for project alignment; empirical benefit untested','review_status':'waived'}]}
reference={'schema':'academic-figure/ReferenceAnalysis@1','reference_id':'abot-agentos-figure1','source':{'url_or_absolute_path':'https://arxiv.org/html/2607.10350v3/figure/agent_v7.png','local_absolute_path':str(HERE/'reference/abot-agentos-figure1.png'),'page_or_figure':'Figure 1','caption':'System architecture of the proposed robot agent (ABot-AgentOS).'},'semantic_structure':{'components':['input','skills/tools','two model tiers','agent harness','memory system','robot hardware'],'groups':['central layers','two sidebars'],'edges':['input to runtime','runtime to hardware','runtime with skills','runtime with memory'],'reading_order':'input → central stack → robot','uncertainties':[]},'style_grammar':grammar,'transfer_policy':{'reuse':['panel composition','color family','typographic hierarchy','roundness','simple icons'],'do_not_copy':['two-model edge/cloud routing','private/common memory','robot brands','specific skills','paper performance claims']},'confidence':'high'}
for name,obj in [('figure-spec.json',spec),('figure-plan.json',plan),('reference-analysis.json',reference)]:
    (HERE/'design'/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
parser=argparse.ArgumentParser(); parser.add_argument('--prepare-only',action='store_true'); args=parser.parse_args()
if not args.prepare_only:
    validator=Path.home()/'.codex/skills/academic-figure-designer/scripts/validate_figure_spec.py'
    if validator.exists():
        subprocess.run(['python3',str(validator),'--strict-v1','--render-ready','--workspace-root',str(ROOT),str(HERE/'design/figure-spec.json')],check=True)
    OUT.write_text(svg)
    print(OUT)
