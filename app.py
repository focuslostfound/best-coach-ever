"""
Best Coach Ever - Curriculum Generation Application
Main Streamlit application for generating sports curriculum using the Enhanced Methodology V3
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

# Get the directory where this script is located
APP_DIR = Path(__file__).parent
METHODOLOGY_PATH = APP_DIR / "METHODOLOGY-ENHANCED-V3-COMPLETE.md"

# Page configuration
st.set_page_config(
    page_title="Best Coach Ever - Curriculum Generator",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'home'
    
    if 'sport' not in st.session_state:
        st.session_state.sport = None
    
    if 'dl_range' not in st.session_state:
        st.session_state.dl_range = None
    
    if 'phases' not in st.session_state:
        st.session_state.phases = None
    
    if 'plays' not in st.session_state:
        st.session_state.plays = None
    
    if 'steps' not in st.session_state:
        st.session_state.steps = None
    
    if 'teaching_blocks' not in st.session_state:
        st.session_state.teaching_blocks = None
    
    if 'dl_assignments' not in st.session_state:
        st.session_state.dl_assignments = None
    
    if 'drills' not in st.session_state:
        st.session_state.drills = None
    
    if 'generation_start_time' not in st.session_state:
        st.session_state.generation_start_time = None
    
    if 'api_client' not in st.session_state:
        # Initialize Anthropic client
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            st.error("⚠️ ANTHROPIC_API_KEY not found in environment variables!")
            st.info("Please add your API key in Streamlit Cloud Settings → Secrets")
            st.stop()
        st.session_state.api_client = Anthropic(api_key=api_key)
    
    # Check for methodology file
    if not METHODOLOGY_PATH.exists():
        st.error(f"⚠️ Methodology file not found!")
        st.info(f"Expected location: {METHODOLOGY_PATH}")
        st.info("Please upload METHODOLOGY-ENHANCED-V3-COMPLETE.md to your repository")
        st.stop()

# Initialize
init_session_state()

# Sidebar with navigation and info
with st.sidebar:
    st.title("🏒 Best Coach Ever")
    st.markdown("### Curriculum Generator")
    st.markdown("---")
    
    # Show current stage
    stages = {
        'home': '🏠 Home',
        'phase_approval': '1️⃣ Phase Approval',
        'play_approval': '2️⃣ Play Approval',
        'auto_generation': '⚙️ Auto-Generation',
        'results': '✅ Results'
    }
    
    st.markdown(f"**Current Stage:**")
    st.info(stages.get(st.session_state.stage, 'Unknown'))
    
    st.markdown("---")
    
    # Show selected parameters
    if st.session_state.sport:
        st.markdown("**Selected Sport:**")
        st.write(st.session_state.sport)
    
    if st.session_state.dl_range:
        st.markdown("**Target DL Range:**")
        st.write(f"{st.session_state.dl_range[0]} - {st.session_state.dl_range[1]}")
    
    st.markdown("---")
    
    # Progress summary
    if st.session_state.stage != 'home':
        st.markdown("**Generation Progress:**")
        progress_items = [
            ("Phases", st.session_state.phases is not None),
            ("Plays", st.session_state.plays is not None),
            ("Steps", st.session_state.steps is not None),
            ("Teaching Blocks", st.session_state.teaching_blocks is not None),
            ("DL Assignments", st.session_state.dl_assignments is not None),
            ("Drills", st.session_state.drills is not None)
        ]
        
        for item_name, is_complete in progress_items:
            icon = "✅" if is_complete else "⬜"
            st.markdown(f"{icon} {item_name}")
    
    st.markdown("---")
    st.markdown("*Based on Methodology v3.0*")

# Main content area
def render_home_screen():
    """Render the home screen with sport selection and DL range"""
    st.title("🏒 Best Coach Ever Curriculum Generator")
    st.markdown("### Generate Complete Sports Curriculum Using Enhanced Methodology V3")
    
    st.markdown("""
    This application generates comprehensive sports curriculum following the enhanced methodology:
    - **Phases** → Game situations
    - **Plays** → Tactical responses (with approval checkpoints)
    - **Steps** → Detailed movement sequences (auto-generated)
    - **Teaching Blocks** → Reusable patterns (auto-generated)
    - **DL Assignments** → When to teach (auto-generated)
    - **Drills** → Practice activities (auto-generated)
    """)
    
    st.markdown("---")
    
    # Sport selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Select Sport")
        sport = st.selectbox(
            "Choose a sport:",
            ["Ice Hockey", "Basketball", "Soccer", "Lacrosse"],
            index=0,
            help="Currently supports Ice Hockey with expansion capability"
        )
    
    with col2:
        st.markdown("### 2. Select Target DL Range")
        dl_range_option = st.radio(
            "Development Level Range:",
            ["DL 1-6 (Recreational Focus)", "DL 1-10 (Full Competitive)"],
            help="DL 1-6 covers recreational/house league. DL 1-10 includes competitive levels."
        )
        
        if dl_range_option == "DL 1-6 (Recreational Focus)":
            dl_range = (1, 6)
        else:
            dl_range = (1, 10)
    
    st.markdown("---")
    
    # Display information about the process
    st.markdown("### 📋 Generation Process")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Interactive Steps (You Approve):**
        1. ✋ **Phase Generation** - Review and approve game phases
        2. ✋ **Play Generation** - Review and approve plays for each phase
        """)
    
    with col2:
        st.markdown("""
        **Automated Steps (Runs to Completion):**
        3. ⚙️ **Step Generation** - Detailed movement sequences
        4. ⚙️ **Teaching Block Identification** - Pattern analysis
        5. ⚙️ **DL Assignment** - When to teach each block
        6. ⚙️ **Drill Generation** - Complete practice drills
        """)
    
    st.markdown("---")
    
    # Estimated time
    st.info("""
    ⏱️ **Estimated Generation Time:**
    - Phase & Play Approval: 5-10 minutes (interactive)
    - Auto-Generation: 15-30 minutes (automated, cannot be interrupted)
    - Total: 20-40 minutes for complete curriculum
    """)
    
    st.markdown("---")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Generate Curriculum", type="primary", use_container_width=True):
            # Save selections to session state
            st.session_state.sport = sport
            st.session_state.dl_range = dl_range
            st.session_state.generation_start_time = datetime.now()
            
            # Move to phase approval stage
            st.session_state.stage = 'phase_approval'
            st.rerun()

def render_phase_approval_screen():
    """Render the phase approval screen"""
    st.title("1️⃣ Phase Approval")
    st.markdown(f"### Sport: {st.session_state.sport}")
    
    st.info("Generating phases using Expert Debate System (5 personas)...")
    
    # Placeholder for phase generation
    st.markdown("Phase generation will be implemented next...")
    
    # For now, show back button
    if st.button("← Back to Home"):
        st.session_state.stage = 'home'
        st.rerun()

def render_play_approval_screen():
    """Render the play approval screen"""
    st.title("2️⃣ Play Approval")
    st.markdown(f"### Sport: {st.session_state.sport}")
    
    st.info("Play approval screen - to be implemented...")
    
    if st.button("← Back to Phases"):
        st.session_state.stage = 'phase_approval'
        st.rerun()

def render_auto_generation_screen():
    """Render the auto-generation progress screen"""
    st.title("⚙️ Auto-Generation in Progress")
    st.markdown("### Generating Complete Curriculum")
    
    st.warning("⚠️ This process cannot be interrupted. Please wait for completion.")
    
    st.info("Auto-generation screen - to be implemented...")

def render_results_screen():
    """Render the results and export screen"""
    st.title("✅ Curriculum Generation Complete!")
    st.markdown(f"### Sport: {st.session_state.sport}")
    
    st.success("Results screen - to be implemented...")
    
    if st.button("🏠 Start New Curriculum"):
        # Reset all session state
        for key in list(st.session_state.keys()):
            if key not in ['api_client']:
                del st.session_state[key]
        st.session_state.stage = 'home'
        st.rerun()

# Main routing logic
def main():
    """Main application routing"""
    
    if st.session_state.stage == 'home':
        render_home_screen()
    
    elif st.session_state.stage == 'phase_approval':
        render_phase_approval_screen()
    
    elif st.session_state.stage == 'play_approval':
        render_play_approval_screen()
    
    elif st.session_state.stage == 'auto_generation':
        render_auto_generation_screen()
    
    elif st.session_state.stage == 'results':
        render_results_screen()
    
    else:
        st.error(f"Unknown stage: {st.session_state.stage}")
        if st.button("Return to Home"):
            st.session_state.stage = 'home'
            st.rerun()

# Run the application
if __name__ == "__main__":
    main()
