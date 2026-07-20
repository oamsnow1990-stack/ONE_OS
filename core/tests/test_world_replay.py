from core.kernel.world_state_manager import WorldStateManager

def run_replay_test():
    manager = WorldStateManager()
    
    print("--- 1. Generating Events ---")
    events = [
        ("UPDATE_DEVICE", {"door": "locked"}),
        ("DETECT_THREAT", {"threat": "intruder_detected"}),
        ("UPDATE_RESOURCE", {"battery": 85}),
        ("UPDATE_DEVICE", {"camera": "recording"})
    ]
    
    for event_name, payload in events:
        manager.commit(event_name, payload)
        print(f"Committed: {event_name} | Version: {manager.get_state().version}")

    final_state = manager.get_state()
    print(f"\nFinal State (v{final_state.version}): {final_state.devices}, {final_state.threats}")
    
    # ดึง Log ออกมา
    event_log = manager._event_log
    
    print("\n--- 2. Resetting & Replaying ---")
    # สร้าง Manager ใหม่ให้เป็นค่าเริ่มต้น
    replayed_manager = WorldStateManager()
    
    # Replay!
    for entry in event_log:
        replayed_manager.commit(entry["event"], entry["payload"])
        
    replayed_state = replayed_manager.get_state()
    print(f"Replayed State (v{replayed_state.version}): {replayed_state.devices}, {replayed_state.threats}")
    
    # ตรวจสอบความถูกต้อง
    if final_state == replayed_state:
        print("\n✅ SUCCESS: Replayed state matches original state perfectly!")
    else:
        print("\n❌ FAILED: States do not match.")

if __name__ == "__main__":
    run_replay_test()