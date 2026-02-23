export default function ProfilePage() {
  return (
    <div className="flex flex-1 overflow-auto">
      <div className="flex h-full w-full flex-1 flex-col gap-4 rounded-tl-2xl border border-gray-200 border-l-0 bg-white p-6 shadow-sm md:p-10">
        <h1 className="text-2xl font-semibold text-gray-900">Profile</h1>
        <p className="text-gray-600">Your profile settings.</p>
      </div>
    </div>
  );
}
