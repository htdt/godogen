## Thread <- RefCounted

A unit of execution in a process. Can run methods on Objects simultaneously. The use of synchronization via Mutex or Semaphore is advised if working with shared objects. **Warning:** To ensure proper cleanup without crashes or deadlocks, when a Thread's reference count reaches zero and it is therefore destroyed, the following conditions must be met: - It must not have any Mutex objects locked. - It must not be waiting on any Semaphore objects. - `wait_to_finish` should have been called on it.

**Methods:**
- get_id() -> String - Returns the current Thread's ID, uniquely identifying it among all threads. If the Thread has not started running or if `wait_to_finish` has been called, this returns an empty string.
- is_alive() -> bool - Returns `true` if this Thread is currently running the provided function. This is useful for determining if `wait_to_finish` can be called without blocking the calling thread. To check if a Thread is joinable, use `is_started`.
- is_main_thread() -> bool - Returns `true` if the thread this method was called from is the main thread. **Note:** This is a static method and isn't associated with a specific Thread object.
- is_started() -> bool - Returns `true` if this Thread has been started. Once started, this will return `true` until it is joined using `wait_to_finish`. For checking if a Thread is still executing its task, use `is_alive`.
- set_thread_safety_checks_enabled(enabled: bool) - Sets whether the thread safety checks the engine normally performs in methods of certain classes (e.g., Node) should happen **on the current thread**. The default, for every thread, is that they are enabled (as if called with `enabled` being `true`). Those checks are conservative. That means that they will only succeed in considering a call thread-safe (and therefore allow it to happen) if the engine can guarantee such safety. Because of that, there may be cases where the user may want to disable them (`enabled` being `false`) to make certain operations allowed again. By doing so, it becomes the user's responsibility to ensure thread safety (e.g., by using Mutex) for those objects that are otherwise protected by the engine. **Note:** This is an advanced usage of the engine. You are advised to use it only if you know what you are doing and there is no safer way. **Note:** This is useful for scripts running on either arbitrary Thread objects or tasks submitted to the WorkerThreadPool. It doesn't apply to code running during Node group processing, where the checks will be always performed. **Note:** Even in the case of having disabled the checks in a WorkerThreadPool task, there's no need to re-enable them at the end. The engine will do so.
- start(callable: Callable, priority: int = 1) -> int - Starts a new Thread that calls `callable`. If the method takes some arguments, you can pass them using `Callable.bind`. The `priority` of the Thread can be changed by passing a value from the `Priority` enum. Returns `OK` on success, or `ERR_CANT_CREATE` on failure.
- wait_to_finish() -> Variant - Joins the Thread and waits for it to finish. Returns the output of the Callable passed to `start`. Should either be used when you want to retrieve the value returned from the method called by the Thread or before freeing the instance that contains the Thread. To determine if this can be called without blocking the calling thread, check if `is_alive` is `false`.

**Enums:**
**Priority:** PRIORITY_LOW=0, PRIORITY_NORMAL=1, PRIORITY_HIGH=2
  - PRIORITY_LOW: A thread running with lower priority than normally.
  - PRIORITY_NORMAL: A thread with a standard priority.
  - PRIORITY_HIGH: A thread running with higher priority than normally.

